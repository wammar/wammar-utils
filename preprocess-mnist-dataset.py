def get_data_and_labels(images_filename, labels_filename):
    print("Opening files ...")
    images_file = open(images_filename, "rb")
    labels_file = open(labels_filename, "rb")

    try:
        print("Reading files ...")
        images_file.read(4)
        num_of_items = int.from_bytes(images_file.read(4), byteorder="big")
        num_of_rows = int.from_bytes(images_file.read(4), byteorder="big")
        num_of_colums = int.from_bytes(images_file.read(4), byteorder="big")
        labels_file.read(8)

        num_of_image_values = num_of_rows * num_of_colums
        data = [[None for x in range(num_of_image_values)]
                for y in range(num_of_items)]
        labels = []
        for item in range(num_of_items):
            print("Current image number: %7d" % item)
            for value in range(num_of_image_values):
                data[item][value] = int.from_bytes(images_file.read(1),
                                                   byteorder="big")
            labels.append(int.from_bytes(labels_file.read(1), byteorder="big"))
        return data, labels
    finally:
        images_file.close()
        labels_file.close()
        print("Files closed.")

def write_sofia_ml_format(data, labels, filename):
    with open(filename, 'w') as f:
        assert(len(data) == len(labels))
        for i in range(len(data)):
            f.write('{} 0:1 '.format(labels[i]))
            for j in range(len(data[i])):
                if data[i][j] == 0: continue
                f.write('{}:{} '.format(j+1, data[i][j]/255.0))
            f.write('\n')

def write_arff_format(data, labels, filename):
    with open(filename, 'w') as f:
        assert(len(data) == len(labels))
        # write arff header
        f.write('@RELATION mnist/{}\n'.format(filename))
        for j in range(len(data[0])):
            f.write('@ATTRIBUTE a{} REAL\n'.format(j))
        f.write('@ATTRIBUTE class {0,1,2,3,4,5,6,7,8,9}\n')
        f.write('@DATA\n')
        # write arff data
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == 0: continue
                f.write('{},'.format(data[i][j]/255.0))
            f.write('{}\n'.format(labels[i]))

# standard mnist
#train_data, train_labels = get_data_and_labels("mnist-raw/train-images-idx3-ubyte", "mnist-raw/train-labels-idx1-ubyte")
#test_data, test_labels = get_data_and_labels(   "mnist-raw/t10k-images-idx3-ubyte",  "mnist-raw/t10k-labels-idx1-ubyte")
#write_sofia_ml_format(train_data, train_labels, "train.sofia")
#write_sofia_ml_format(test_data, test_labels, "test.sofia")
#write_arff_format(train_data, train_labels, "train.arff")
#write_arff_format(test_data, test_labels, "test.arff")

# 8 million mnist (train only)
train8m_data, train8m_labels = get_data_and_labels("mnist-raw/mnist8m-patterns-idx3-ubyte", "mnist-raw/mnist8m-labels-idx1-ubyte")
write_sofia_ml_format(train_data, train_labels, "train8m.sofia")
write_arff_format(train_data, train_labels, "train8m.arff")
