import io

with io.open('/usr/local/google/home/wammar/data/iris/iris.data') as in_file, io.open('/usr/local/google/home/wammar/data/iris/iris.data.pre', mode='w') as out_file:

  # label string->int
  label_map = {}

  # process data set
  print 'processing data...'
  examples_count = 0
  for labeled_example in in_file:
    splits = labeled_example.strip().split(',')
    feature_values, label = splits[:-1], splits[-1]
    if label not in label_map: label_map[label] = len(label_map)
    label = label_map[label]
    # check format. it's a ternary classification task.
    if label != 0 and label != 1 and label != 2:
      print 'label = ', label, ' and labeled_example = ', labeled_example
    assert(label == 0 or label == 1 or label == 2)
    # check format. each example has 4 features.
    if len(feature_values) != 4:
      print 'len(feature_values) = ', len(feature_values), ' != 4, after processing ', examples_count, 'examples.'
      assert False
    # write gold label
    out_file.write(unicode(label))
    # all features are active
    for feature_id in xrange(0, len(feature_values)):
      feature_value = feature_values[feature_id]
      out_file.write(u' {}:{}'.format(feature_id+1, feature_value))
    out_file.write(u'\n')
    # update counter
    examples_count += 1

  # check format.
  if examples_count != 150:
    print 'examples_count = ', examples_count, ' != 150, something is wrong, the iris dataset contains 150 examples.'
    assert False

  # done
  print examples_count, ' training examples processed.'
