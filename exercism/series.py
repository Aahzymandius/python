def slices(series, length):
  slices=[,]
  for i in range(len(series) - length + 1):
    slices[i]=series[i:i+length]

  return slices
