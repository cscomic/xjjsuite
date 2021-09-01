from multiprocessing import Pool


# class _ThreadData(Pool):
#     """
#     Represents thread independent data
#     """
#
#     def __init__(self):
#         self.reset()
#
#     def reset(self):
#         """
#         Resets thread data model
#         """
#
#         self.disableStdOut = False
#         self.hashDBCursor = None
#         self.inTransaction = False
#         self.lastCode = None
#         self.lastComparisonPage = None
#         self.lastComparisonHeaders = None
#         self.lastComparisonCode = None
#         self.lastComparisonRatio = None
#         self.lastErrorPage = tuple()
#         self.lastHTTPError = None
#         self.lastRedirectMsg = None
#         self.lastQueryDuration = 0
#         self.lastPage = None
#         self.lastRequestMsg = None
#         self.lastRequestUID = 0
#         self.lastRedirectURL = tuple()
#         # self.random = WichmannHill()
#         self.resumed = False
#         self.retriesCount = 0
#         # self.seqMatcher = difflib.SequenceMatcher(None)
#         # self.shared = shared
#         self.technique = None
#         self.validationRun = 0
#         self.valueStack = []
#
#
# ThreadData = _ThreadData()


def runThreads(numThreads: int, threadFunction, arg):
    pool = Pool(processes=numThreads)
    pool.apply_async(threadFunction, (arg,))
    pool.close()
    pool.join()
