// This file contains methods extending the Value class. 

//
// Value
//
%extend CNTK::Value {
    static CNTK::ValuePtr CNTK::Value::CreateDenseFloat(const CNTK::NDShape& sampleShape, const std::vector<std::vector<float>>& sequences,
        const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::Create<float>(sampleShape, sequences, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateDenseDouble(const CNTK::NDShape& sampleShape, const std::vector<std::vector<double>>& sequences,
        const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::Create<double>(sampleShape, sequences, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateDenseFloat(const CNTK::NDShape& sampleShape, const std::vector<std::vector<float>>& sequences,
        const std::vector<bool>& sequenceStartFlags, const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::Create<float>(sampleShape, sequences, sequenceStartFlags, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateDenseDouble(const CNTK::NDShape& sampleShape, const std::vector<std::vector<double>>& sequences,
        const std::vector<bool>& sequenceStartFlags, const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::Create<double>(sampleShape, sequences, sequenceStartFlags, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateOneHotFloat(size_t dimension, const std::vector<std::vector<size_t>>& oneHotSequences,
        const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::Create<float>(dimension, oneHotSequences, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateOneHotDouble(size_t dimension, const std::vector<std::vector<size_t>>& oneHotSequences,
        const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::Create<double>(dimension, oneHotSequences, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateOneHotFloat(size_t dimension, const std::vector<std::vector<size_t>>& oneHotSequences,
        const std::vector<bool>& sequenceStartFlags, const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::Create<float>(dimension, oneHotSequences, sequenceStartFlags, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateOneHotDouble(size_t dimension, const std::vector<std::vector<size_t>>& oneHotSequences,
        const std::vector<bool>& sequenceStartFlags, const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::Create<double>(dimension, oneHotSequences, sequenceStartFlags, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateSequenceFloat(const CNTK::NDShape& sequenceShape,
        const CNTK::SparseIndexType* colStarts, const CNTK::SparseIndexType* rowIndices, const float* nonZeroValues, size_t numNonZeroValues,
        bool sequenceStartFlag, const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::CreateSequence<float>(sequenceShape, colStarts, rowIndices, nonZeroValues, numNonZeroValues, sequenceStartFlag, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateSequenceDouble(const CNTK::NDShape& sequenceShape,
        const CNTK::SparseIndexType* colStarts, const CNTK::SparseIndexType* rowIndices, const double* nonZeroValues, size_t numNonZeroValues,
        bool sequenceStartFlag, const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::CreateSequence<double>(sequenceShape, colStarts, rowIndices, nonZeroValues, numNonZeroValues, sequenceStartFlag, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateSequenceFloat(const CNTK::NDShape& sequenceShape,
        const CNTK::SparseIndexType* colStarts, const CNTK::SparseIndexType* rowIndices, const float* nonZeroValues, size_t numNonZeroValues,
        const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::CreateSequence<float>(sequenceShape, colStarts, rowIndices, nonZeroValues, numNonZeroValues, device, readOnly);
    }

    static CNTK::ValuePtr CNTK::Value::CreateSequenceDouble(const CNTK::NDShape& sequenceShape,
        const CNTK::SparseIndexType* colStarts, const CNTK::SparseIndexType* rowIndices, const double* nonZeroValues, size_t numNonZeroValues,
        const CNTK::DeviceDescriptor& device, bool readOnly = false) {
        return CNTK::Value::CreateSequence<double>(sequenceShape, colStarts, rowIndices, nonZeroValues, numNonZeroValues, device, readOnly);
    }

}