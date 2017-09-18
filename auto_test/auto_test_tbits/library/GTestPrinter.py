class GTestPrinter:
	HEADER = '\033[0;32m'
	OKBLUE = '\033[0;34m'
	OKGREEN = '\033[0;32m'
	WARNING = '\033[0;33m'
	FAIL = '\033[0;31m'
	ENDC = '\033[0m'

	@staticmethod
	def print_head():
		return GTestPrinter.HEADER + '[==========]' + GTestPrinter.ENDC

	@staticmethod
	def print_run():
		return GTestPrinter.HEADER + '[ RUN      ]' + GTestPrinter.ENDC

	@staticmethod
	def print_ok():
		return GTestPrinter.HEADER + '[       OK ]' + GTestPrinter.ENDC

	@staticmethod
	def print_error():
		return GTestPrinter.FAIL + '[  FAILED  ]' + GTestPrinter.ENDC
