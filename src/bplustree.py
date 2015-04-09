M = 10
myServerId = 'S05'
class Leaf(object):
	'''
	Leaf nodes for the bplus tree.
	One dimensional keys, their count, corresponding object pointers are stored
	Parent, left sibling, right sibling also stored for efficiency
	'''
	def __init__(self):
		self.keyCount = 0
		self.key = []
		self.ptr = []
		for i in range(0,M):
			self.key.append(2.000000)
			self.ptr.append({'serverID' : 'SXX', 'fileName': 'unoccupied'})
		self.parent = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
		self.left = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
		self.right = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
	
	def printToFile(self, fileName):
		# to print node content to file.
		with open(fileName, 'w+') as f:
			f.write(str(self.keyCount)+'\n')
			for i in range(0, M):
				f.write('{0:.6f}\t'.format(self.key[i]))
			f.write('\n')
			for i in range(0, M):
				f.write(self.ptr[i]['serverID']+'\t')
				f.write(self.ptr[i]['fileName']+'\t')
			f.write('\n' + self.parent['serverID'] + '\t' + self.parent['fileName'])
			f.write('\n' + self.left['serverID'] + '\t' + self.left['fileName'])
			f.write('\n' + self.right['serverID'] + '\t' + self.right['fileName'])
			# TODO append garbage

	def readFromFile(self, fileName):
		f = open(fileName, 'r')
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		sidFiles = (lines[2].strip().split('\t'))
		self.ptr = []
		for i in range(0, len(sidFiles), 2):
			self.ptr.append({'serverID' : sidFiles[i], 'fileName': sidFiles[i+1]})

		sidFile = lines[3].strip().split('\t')
		self.parent = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		sidFile = lines[4].strip().split('\t')
		self.left = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		sidFile = lines[5].strip().split('\t')
		self.right = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		f.close()

class Node(object):
	'''
	Internal nodes for the bplus tree.
	One dimensional keys, their count, corresponding child pointers are stored
	Parent also stored for efficiency
	'''
	def __init__(self):
		self.keyCount = 0
		self.key = []
		self.ptr = []
		for i in range(0,M):
			self.key.append(2.000000)
			self.ptr.append({'serverID' : 'SXX', 'fileName': 'unoccupied'})
		self.ptr.append({'serverID' : 'SXX', 'fileName': 'unoccupied'}) # M + 1 pointers
		self.parent = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
	
	def printToFile(self, fileName):
		# to print node content to file.
		with open(fileName, 'w+') as f:
			f.write(str(self.keyCount)+'\n')
			for i in range(0, M):
				f.write('{0:.6f}\t'.format(self.key[i]))
			f.write('\n')
			for i in range(0, M):
				f.write(self.ptr[i]['serverID']+'\t')
				f.write(self.ptr[i]['fileName']+'\t')
			
			f.write(self.ptr[i]['serverID']+'\t') # M+1 pointers
			f.write(self.ptr[i]['fileName']+'\t')
			f.write('\n' + self.parent['serverID'] + '\t' + self.parent['fileName'])

	def readFromFile(self, fileName):
		f = open(fileName, 'r')
		lines = f.readlines()
		self.keyCount = int(lines[0])
		self.key = (lines[1].strip().split('\t'))
		self.key = [float(x) for x in self.key]
		sidFiles = (lines[2].strip().split('\t'))
		self.ptr = []
		for i in range(0, len(sidFiles), 2):
			self.ptr.append({'serverID' : sidFiles[i], 'fileName': sidFiles[i+1]})

		sidFile = lines[3].strip().split('\t')
		self.parent = {'serverID' : sidFile[0], 'fileName': sidFile[1]}
		f.close()

def isLeaf(s):
	return s[0] == 'L'

def stringify(a, b):
	return a + "$" + b

def stringifyLeaf(leaf):
	string = str(leaf.keyCount)
	for i in range(0, M):
		string = string + "$" + str(leaf.key[i])
	for i in range(0, M):
		string = string + "$" + leaf.ptr[i]['serverID'] + "$" + leaf.ptr[i]['fileName']
	string = string + "$" + leaf.parent['serverID'] + "$" + leaf.parent['fileName']
	string = string + "$" + leaf.left['serverID'] + "$" + leaf.left['fileName']
	string = string + "$" + leaf.right['serverID'] + "$" + leaf.right['fileName']
	return string

def stringifyNode(node):
	string = str(node.keyCount)
	for i in range(0, M):
		string = string + "$" + str(node.key[i])
	for i in range(0, M+1):
		string = string + "$" + node.ptr[i]['serverID'] + "$" + node.ptr[i]['fileName']
	string = string + "$" + node.parent['serverID'] + "$" + node.parent['fileName']
	return string

def findLeaf(key, fileName):
	if isLeaf(fileName):
		response = stringify(myServerId, fileName)
		return response
	else:
		n = Node()
		n.readFromFile(fileName)
		for i in range(0, n.keyCount+1):
			if i == n.keyCount or key <= n.key[i]:
				pass
		# TODO get the childNode = (serverID, fileName) dict from n.ptr[i]
		childNode = { 'serverID' : 'S05', 'fileName' : 'F0001'}
		if childNode['serverID'] == myServerId:
			result = findLeaf(key, childNode['fileName'])
		else:
			query = 'FINDLEAF$'+str(key)+'$'+childNode['fileName']
			result = client.request(childNode['serverID'], query)
		return result


def splitNode(myNode):
	pass
	# get middle key.
	# make call to central server to getNewNode().
	# prepare content to write on this new file
	# make changes to current myNode
	# inform half of the children about change of their parent

	# if current one is a ROOT (of tree) node
	# make appropriate changes. new root setting
	# else inform parent about new sibling

def insertInNode(myNode, key, child):
	pass
	# assert that insertion file is in this server
	# open file, read, find position, insert
	# adjust child pointers, keycount++
	# now if size limits, split

def insertInLeaf(leafName, key, ptr):
	n = Leaf()
	n.readFromFile(leafName)
	position = 0
	
	while position < n.keyCount and n.key[position] <= key:
		position += 1
	
	for i in range(n.keyCount, position, -1):
		n.key[i] = n.key[i-1]
		n.ptr[i] = n.ptr[i-1]
	
	n.key[position] = key
	n.ptr[position] = ptr
	n.keyCount += 1
	n.printToFile(leafName)

	if n.keyCount == M:
		splitLeaf(leafName)

	return "SUCCESS"


# a = Leaf()
# a.printToFile('whatever')
# a.readFromFile('whatever')
# print a.parent