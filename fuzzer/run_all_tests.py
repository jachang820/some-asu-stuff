#!/usr/bin/python3

from subprocess import Popen, PIPE

prog_files = ["./progs/prog{0}/prog_{0}".format(i) for i in range(3)]
prog_files.extend("./progs/prog_" + str(i) for i in range(10))

seed_files = ["./progs/prog{0}/seed".format(i) for i in range(3)]

solution_files = ["./solutions/prog_{0}.txt".format(i) for i in range(3)]
solution_files.extend("./solutions/test_suite/prog_{0}.txt".format(i) 
  for i in range(10))


for test_num, prog_file in enumerate(prog_files):
  # Only first 3 progs have initial seeds.
  seed_file = seed_files[test_num] if test_num < 3 else False
  solution = solution_files[test_num]

  try:
    with open(solution, 'r') as f:
      prng_seed, num_iterations = f.read().split(' ')
  except:
    print("A solution for {0} does not exist.".format(prog_file))
    continue

  # num_iterations = str(int(num_iterations) + 1000)
  argv = ["./fuzzer", prng_seed, num_iterations]
  if seed_file:
    argv.append(seed_file)

  num_seg_faults = 0
  for j in range(100):
    # Run fuzzer and pipe output into program to test.
    fuzzer = Popen(argv, stdout=PIPE)
    testprog = Popen([prog_file], stdin=fuzzer.stdout)

    try:
      # prog_6 and prog_7 seem to run on infinite loops.
      # Kill prog if test runs too long.
      out, err = testprog.communicate(timeout=0.5)
    except:
      pass

    SEGMENTATION_FAULT = -11
    if testprog.returncode == SEGMENTATION_FAULT:
      num_seg_faults += 1

  print("./fuzzer {0} {1} {2}| {3} --> {4}/100 Segmentation fault".format(
    prng_seed, 
    num_iterations,
    seed_file + " " if seed_file else "",
    prog_file,
    num_seg_faults))
