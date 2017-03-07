# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

import sys
import numpy as np

from cntk import cntk_py

from cntk import output_variable, Constant, Parameter, CloneMethod

from cntk.ops.functions import Function, UserFunction

__doc__ = '''
In order to debug a graph one simply needs to wrap the root node as follows::

    # ... setting up the model in z
    from cntk.debug import debug_model
    z = debug_model(z)

Then, when ``z`` is evaluated or trained (i.e. when either
:meth:`~cntk.ops.functions.Function.forward` or
:meth:`~cntk.ops.functions.Function.backward` is called, you will see the
following command-line interface::

    Forward after Parameter node with uid='Parameter28' shape=[](2,)
    [CNTK forward] >>> help
    Commands:
        n - execute the next node
        n <number> - execute the next <number> nodes
        n <lambda> - execute until the lambda expression is True. Examples:
                     Until a Times node is hit:
                         lambda arg, node: node.op_name == 'Times'
                     Until a node is hit that has 3 dimensions:
                         lambda arg, node: len(node.shape) == 3
                     Until the variance of the input exceeds 1 (np = numpy):
                         lambda arg, node: np.var(arg) > 1
        f - run until forward pass (like 'n' when already in forward pass)
        b - run until backward pass (like 'n' when already in backward pass)
        c - run until end
        p - print input (forward) or root gradients (backward)
        d - drop into a pdb shell
        q - quit

    [CNTK backward] >>> n

    ======================================== forward  ========================================
    Forward after Parameter node with uid='Parameter28' shape=[](2,)
    [CNTK forward] >>> n
    Forward after Times node with uid='Times29' shape=[*,*](2,)
    [CNTK forward] >>> n
    ======================================== backward ========================================
    Backward before Times node with uid='Times29' shape=[*,*](2,)
    [CNTK backward] >>> p
    State: None
    Root gradients:
    [[[-0.79412955  0.79412955]]
    
     [[-0.79412955  0.79412955]]
    
     [[ 0.20587046 -0.20587045]]
    
     [[ 0.20587046 -0.20587045]]
    
     [[ 0.20587046 -0.20587045]]
    
     [[ 0.20587046 -0.20587045]]
    
     [[-0.79412955  0.79412955]]
    
     [[ 0.20587046 -0.20587045]]
    
     [[ 0.20587039 -0.20587039]]
    
     [[-0.79412961  0.79412961]]]

At every stop the following information is given:
 * Forward or backward pass
 * Node type (e.g. 'Times')
 * Name if given, otherwise it is omitted
 * uid, which is a unique reference within the graph
 * shape having the format [dynamic axis](static axes). E.g. ``[*,*](2,)``
   means that the node's output has two dynamic axes (batch and sequence) and
   one static axis (2 dimensions)
'''


def save_as_legacy_model(root_op, filename):
    '''
    Save the network of ``root_op`` in ``filename``.
    For debugging purposes only, very likely to be deprecated in the future.

    Args:
        root_op (:class:`~cntk.functions.Function`): op of the graph to save
        filename (str): filename to store the model in.
    '''
    cntk_py.save_as_legacy_model(root_op, filename)


class DebugNode(UserFunction):
    '''
    A user function that exposes a command line interface. With that one can
    step through the graph and investigate data, shapes, etc.
    '''
    _commands = []
    _last_pass = 'f'

    def __init__(self, arg, name='DebugNode'):
        super(DebugNode, self).__init__([arg], as_numpy=True, name=name)
        self.after = arg

    def __wait_for_input(self, prompt):
        understood = False
        while not understood:
            new_input = input(prompt).strip()
            if not new_input:
                continue

            if len(new_input) == 1 and new_input in 'bcdfp':
                understood = [new_input]
            elif new_input[0] == 'n':
                try:
                    if len(new_input) > 1:
                        number = int(new_input[1:])
                    else:
                        number = 1
                    understood = ['n'] * number
                except ValueError:
                    try:
                        code = eval(new_input[1:])
                        understood = [code]
                    except SyntaxError:
                        understood = False
            elif new_input == 'q':
                sys.exit(0)

            if not understood:
                print('''\
Commands:
    n - execute the next node
    n <number> - execute the next <number> nodes
    n <lambda> - execute until the lambda expression is True. Examples:
                 Until a Times node is hit:
                     lambda arg, node: node.op_name == 'Times'
                 Until a node is hit that has 3 dimensions:
                     lambda arg, node: len(node.shape) == 3
                 Until the variance of the input exceeds 1 (np = numpy):
                     lambda arg, node: np.var(arg) > 1
    f - run until forward pass (like 'n' when already in forward pass)
    b - run until backward pass (like 'n' when already in backward pass)
    c - run until end
    p - print input (forward) or root gradients (backward)
    d - drop into a pdb shell
    q - quit
''')

        return understood

    def _format_status(self):
        if isinstance(self.after, Constant):
            node_type = 'Constant'
        elif isinstance(self.after, Parameter):
            node_type = 'Parameter'

        elif isinstance(self.after, Function):
            node_type = self.after.op_name

        else:
            node_type = type(self.after)

        if self.after.is_sparse:
            node_type += ' (sparse)'

        if self.after.name:
            name = "name='%s' " % self.after.name
        else:
            name = ''

        dyn_axes = '[%s]' % ','.join(['*']*len(self.after.dynamic_axes))
        
        return "%s node with %suid='%s' shape=%s%s" % \
               (node_type, name, self.after.uid, dyn_axes, self.after.shape)

    def _print_status(self, current_pass):
        if current_pass != DebugNode._last_pass:
            if current_pass == 'f':
                print()
                print('='*40 + ' forward  ' + '='*40)
            else:
                print('='*40 + ' backward ' + '='*40)

        if current_pass == 'f':
            print("Forward after %s" % self._format_status())
        else:
            print("Backward before %s" % self._format_status())

    def forward(self, argument, device=None, outputs_to_retain=None):
        self._print_status('f')

        commands = DebugNode._commands

        done = False
        while not done:
            if not commands:
                DebugNode._commands = commands = self.__wait_for_input(
                    '[CNTK forward] >>> ')

            if commands[-1] == 'c':
                done = True

            elif commands[-1] == 'n':
                commands.pop()
                done = True

            elif commands[-1] == 'b':
                done = True

            elif commands[-1] == 'f':
                commands.pop()
                done = True

            elif commands[-1] == 'p':
                print('Input: ')
                print(argument)
                commands.pop()

            elif commands[-1] == 'd':
                commands.pop()
                import pdb
                pdb.set_trace()
                done = True

            elif callable(commands[-1]):
                if commands[-1](argument, self.after):
                    commands.pop()
                else:
                    done = True

        DebugNode._last_pass = 'f'

        return None, argument

    def backward(self, state, root_gradients):
        self._print_status('b')

        done = False
        commands = DebugNode._commands
        while not done:
            if not commands:
                DebugNode._commands = commands = self.__wait_for_input(
                    '[CNTK backward] >>> ')

            if commands[-1] == 'c':
                done = True

            elif commands[-1] == 'n':
                commands.pop()
                done = True

            elif commands[-1] == 'b':
                commands.pop()
                done = True

            elif commands[-1] == 'f':
                done = True

            elif commands[-1] == 'p':
                print('State: %s' % str(state))
                print('Root gradients: ')
                print(root_gradients)
                commands.pop()

            elif commands[-1] == 'd':
                import pdb
                pdb.set_trace()
                done = True

            elif callable(commands[-1]):
                if commands[-1](root_gradients, self.after):
                    commands.pop()
                else:
                    done = True

        DebugNode._last_pass = 'b'

        return root_gradients

    def infer_outputs(self):
        return [output_variable(self.inputs[0].shape, self.inputs[0].dtype,
                                self.inputs[0].dynamic_axes)]


def debug_model(model):
    '''
    Returns a cloned model that has debug nodes inserted everywhere. When the
    graph is evaluated or trained, those nodes will allow to inspect the graph.
    '''
    from cntk.graph import depth_first_search
    nodes = depth_first_search(model, lambda x: True)

    mod = {n: DebugNode(n) for n in nodes}
    model = model.clone(CloneMethod.share, mod)

    return model
