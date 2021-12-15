#!/usr/bin/python3

from subprocess import Popen, PIPE


# Note!! prog_8 needs to be tested more smartly.
# Skip prog_8


prog_files = ["./progs/prog{0}/prog_{0}".format(i) for i in range(3)]
prog_files.extend("./progs/prog_" + str(i) for i in range(10))

seed_files = ["./progs/prog{0}/seed".format(i) for i in range(3)]

# Running the loop too long slows down the computer.
# Pick which programs to test at a time.
test_these = [True, True, True,
  True, True, True, True, True,
  True, True, True, False, True]

solutions = {}

for test_num, prog_file in enumerate(prog_files):
  # Only first 3 progs have initial seeds.
  seed_file = seed_files[test_num] if test_num < 3 else False

  if test_these[test_num]:
    print("Testing {0}".format(prog_file))
  else:
    print("Skipped {0}".format(prog_file))
    continue

  for iters in range(15000):
    print("Iteration {0}/15000...".format(iters))

    SEED = 0
    argv = ["./fuzzer", str(SEED), str(iters)]
    if seed_file:
      argv.append(seed_file)
    
    # Run fuzzer and pipe output into program to test.
    fuzzer = Popen(argv, stdout=PIPE)
    testprog = Popen([prog_file], stdin=fuzzer.stdout)
    try:
      # prog_6 and prog_7 seem to run on infinite loops.
      # Kill prog if test runs too long.
      out, err = testprog.communicate(timeout=0.3)
    except:
      pass

    SEGMENTATION_FAULT = -11
    if testprog.returncode == SEGMENTATION_FAULT:
      solutions[prog_file] = iters
      print("{0} -- seed: 0, iters: {1}".format(prog_file, iters))
      break

print("SUMMARY")
for prog_file, iters in solutions.items():
  print("{0} -- seed: 0, iters: {1}".format(prog_file, iters))