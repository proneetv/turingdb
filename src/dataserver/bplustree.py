import client
M = 40
myServerId = 'S01'
centralServerID = client.centralServerID
class BPT:
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
				self.ptr.append('unoccupied')
			self.parent = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
			self.left = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
			self.right = {'serverID' : 'SXX', 'fileName': 'unoccupied'}
		
		def printToFile(self, fileName):
			# to print node content to file.
			fileName = 'data/'+fileName
			with open(fileName, 'w+') as f:
				f.write(str(self.keyCount)+'\n')
				for i in range(0, M):
					f.write('{0:.6f}\t'.format(self.key[i]))
				f.write('\n')
				for i in range(0, M):
					f.write(self.ptr[i]+'\t')
				f.write('\n' + self.parent['serverID'] + '\t' + self.parent['fileName'])
				f.write('\n' + self.left['serverID'] + '\t' + self.left['fileName'])
				f.write('\n' + self.right['serverID'] + '\t' + self.right['fileName'])
				# TODO append garbage

		def readFromFile(self, fileName):
			fileName = 'data/'+fileName
			f = open(fileName, 'r')
			lines = f.readlines()
			self.keyCount = int(lines[0])
			self.key = (lines[1].strip().split('\t'))
			self.key = [float(x) for x in self.key]
			cdnFiles = (lines[2].strip().split('\t'))
			self.ptr = []
			for i in range(0, len(cdnFiles)):
				self.ptr.append(cdnFiles[i])

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
			fileName = 'data/'+fileName
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
			fileName = 'data/'+fileName
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

	def isLeaf(self, s):
		return s[0] == 'L'

	def stringifyLeaf(self, leaf):
		'''
		Takes a leaf object and convert its contents into string with # as separator.
		This will make it easy and uniform way transfer data over network.
		'''
		string = str(leaf.keyCount)
		for i in range(0, M):
			string = string + '#' + str(leaf.key[i])
		for i in range(0, M):
			string = string + '#' + leaf.ptr[i]
		string = string + '#' + leaf.parent['serverID'] + '#' + leaf.parent['fileName']
		string = string + '#' + leaf.left['serverID'] + '#' + leaf.left['fileName']
		string = string + '#' + leaf.right['serverID'] + '#' + leaf.right['fileName']
		return string

	def stringifyNode(self, node):
		'''
		Takes a node object and converts its content into string with # as separator.
		This will make it easy and uniform way transfer data over network.
		'''
		string = str(node.keyCount)
		for i in range(0, M):
			string = string + '#' + str(node.key[i])
		for i in range(0, M+1):
			string = string + '#' + node.ptr[i]['serverID'] + '#' + node.ptr[i]['fileName']
		string = string + '#' + node.parent['serverID'] + '#' + node.parent['fileName']
		return string

	def destringifyLeaf(self, content):
		items = content.split('#')
		l = self.Leaf()
		l.keyCount = items[0]
		j = 1
		for i in range(0, M):
			l.key[i] = float(items[j])
			j+=1
		for i in range(0, M):
			l.ptr[i] = items[j]
			j+=1
		l.parent = {'serverID': items[j], 'fileName': items[j+1]}
		l.left = {'serverID': items[j+2], 'fileName': items[j+3]}
		l.right = {'serverID': items[j+4], 'fileName': items[j+5]}
		return l

	def destringifyNode(self, content):
		items = content.split('#')
		n = self.Node() # hoping this will be returned correctly with destruction.
		n.keyCount = items[0]
		j = 1
		for i in range(0, M):
			n.key[i] = float(items[j])
			j+=1
		for i in range(0, M+1):
			n.ptr[i] = {'serverID': items[j], 'fileName': items[j+1]}
			j+=2
		n.parent = {'serverID': items[j], 'fileName': items[j+1]}
		return n

	def stringifyArray(self, array):
		ans = ''
		if len(array) == 0:
			return ans
		ans = str(array[0])
		for i in range(1, len(array)):
			ans = ans + '$' + str(array[i])
		return ans


	def findLeaf(self, key, fileName):
		'''
		Returns the leaf file corresponding to the key.
		'''
		if self.isLeaf(fileName):
			response = myServerId + '$' + fileName
			return response
		else:
			n = self.Node()
			n.readFromFile(fileName)
			for i in range(0, n.keyCount+1):
				if i == n.keyCount or key <= n.key[i]:
					childNode = n.ptr[i]
					break
			# childNode = { 'serverID' : 'S05', 'fileName' : 'F0001'}
			if childNode['serverID'] == myServerId:
				result = self.findLeaf(key, childNode['fileName']) # local call
			else:
				query = 'FINDLEAF$'+str(key)+'$'+childNode['fileName']
				result = client.request(childNode['serverID'], query) # network call
			return result

	def splitNode(self, fileName):
		'''
		Assumes leaf has M keys, and need to split.
		Find best server for the sibling leaf and pass half data to the sibling.
		Correct left right pointers correspondingly
		Handle case when this leaf is root
		Inform parent about this change
		Inform children about change
		'''
		n = self.Node()
		sib = self.Node()
		nextNode = self.Node()

		n.readFromFile(fileName)
		midKey = n.key[M/2]

		query = 'NEWNODE$' + str(midKey)
		response = client.request(centralServerID, query)
		response = response.split('$')
		# make network call to central server to get best server for this new file using key as a guide
		
		sibling = dict()
		sibling['serverID'] = response[0]
		sibling['fileName'] = response[1]

		# fill details in sibling object and then we make a network call to destination server with stringified leaf
		n.keyCount = M/2
		sib.keyCount = M - M/2 - 1
		for i in range(0, sib.keyCount):
			sib.key[i] = n.key[i + M/2 + 1]
			sib.ptr[i] = n.ptr[i + M/2 + 1]
		sib.ptr[sib.keyCount] = n.ptr[M]
		# children need to be told about their new parent
		if self.isLeaf(sib.ptr[0]['fileName']):
			child = self.Leaf()
		else:
			child = self.Node()
		for i in range(0, sib.keyCount+1):
			node = sib.ptr[i]
			if node['serverID'] != 'SXX':
				if node['serverID'] == myServerId:
					child.readFromFile(node['fileName'])
					child.parent = sibling
					child.printToFile(node['fileName'])
				else:
					# make network call to this server to update parent of this node
					query = 'CHANGEPARENT$' + node['fileName'] + '$' + sibling['serverID'] + '$' + sibling['fileName']
					client.request(node['serverID'], query)

		# If current node is root, handle separately.
		query = 'WHOISROOT'
		response = client.request(centralServerID, query)
		response = response.split('$')
		root = dict()
		root['serverID'] = response[0]
		root['fileName'] = response[1]

		if myServerId == root['serverID'] and fileName == root['fileName']: # this is root
			query = 'NEWNODE$' + str(midKey)
			response = client.request(centralServerID, query)
			response = response.split('$')
			root['serverID'] = response[0]
			root['fileName'] = response[1]
			# usual B+ Node split in case it is the root
			newRoot = self.Node()
			newRoot.key[0] = midKey
			newRoot.ptr[0] = {'serverID': myServerId, 'fileName': fileName}
			newRoot.ptr[1] = {'serverID': sibling['serverID'], 'fileName': sibling['fileName']}
			newRoot.keyCount = 1
			# save these info about root node
			# TODO : can save a network call here if same serverID
			query = 'SAVENODE$' + root['fileName'] + '$' + self.stringifyNode(newRoot)
			response = client.request(root['serverID'], query)
			# ask central server to change the root.
			query = 'CHANGEROOT$' + root['serverID'] + '$' + root['fileName']
			response = client.request(centralServerID, query)
			n.parent = root
			sib.parent = root
			n.printToFile(fileName)
			# print content to files
			if sibling['serverID'] == myServerId:
				sib.printToFile(sibling['fileName'])
			else:
				query = 'SAVENODE$' + sibling['fileName'] + '$' + self.stringifyNode(sib)
				response = client.request(sibling['serverID'], query)
		else:
			# this leaf is not root
			sib.parent = n.parent
			n.printToFile(fileName)
			# print to files
			if sibling['serverID'] == myServerId:
				sib.printToFile(sibling['fileName'])
			else:
				query = 'SAVENODE$' + sibling['fileName'] + '$' + self.stringifyNode(sib)
				response = client.request(sibling['serverID'], query)
				# network call to save sibling file in its host data server
				# now insert midKey | pointer in parent
				parent = n.parent
				if parent['serverID'] == myServerId:
					self.insertInNode(parent['fileName'], midKey, sibling)
				else:
					# make network call here
					query = 'INSERTINNODE$' + parent['fileName'] + '$' + str(midKey) + '$' + sibling['serverID'] + '$' + sibling['fileName']
					client.request(parent['serverID'], query)
		return 'SUCCESS'

	def insertInNode(self, fileName, key, ptr):
		'''
		Assertively, this node resides on this data server. 
		Open that and insert key and corresponding object ptr in this file.
		'''
		n = self.Node()
		n.readFromFile(fileName)
		position = 0
		
		while position < n.keyCount and n.key[position] <= key:
			position += 1
		# appropriate position to insert
		for i in range(n.keyCount, position, -1):
			n.key[i] = n.key[i-1]
			n.ptr[i+1] = n.ptr[i]
		# move one ahead
		n.key[position] = key
		n.ptr[position + 1] = ptr
		n.keyCount += 1
		n.printToFile(fileName)

		if n.keyCount == M:
			self.splitNode(fileName)
			# split has to be handled by the data server whose file is going to split
		return 'SUCCESS'

	def insertInLeaf(self, leafName, key, ptr):
		'''
		Assertively, this leaf resides on this data server. 
		Open that and insert key and corresponding object ptr in this file.
		'''
		n = self.Leaf()
		n.readFromFile(leafName)
		position = 0
		
		while position < n.keyCount and n.key[position] <= key:
			position += 1
		# appropriate position to insert
		for i in range(n.keyCount, position, -1):
			n.key[i] = n.key[i-1]
			n.ptr[i] = n.ptr[i-1]
		# move one ahead
		n.key[position] = key
		n.ptr[position] = ptr
		n.keyCount += 1
		n.printToFile(leafName)

		if n.keyCount == M:
			self.splitLeaf(leafName)
			# split has to be handled by the data server whose file is going to split

		return 'SUCCESS'

	def splitLeaf(self, fileName):
		'''
		Assumes leaf has M keys, and need to split.
		Find best server for the sibling leaf and pass half data to the sibling.
		Correct left right pointers correspondingly
		Handle case when this leaf is root
		Inform parent about this change
		'''
		n = self.Leaf()
		sib = self.Leaf()
		nextLeaf = self.Leaf()

		n.readFromFile(fileName)
		midKey = n.key[M/2]
		
		query = 'NEWLEAF$' + str(midKey)
		response = client.request(centralServerID, query)
		response = response.split('$')
		# make network call to central server to get best server for this new file using key as a guide
		
		sibling = dict()
		sibling['serverID'] = response[0]
		sibling['fileName'] = response[1]

		n.keyCount = M/2
		sib.keyCount = M-M/2
		for i in range(0, sib.keyCount):
			sib.key[i] = n.key[i + M/2]
			sib.ptr[i] = n.ptr[i + M/2]

		# fill details in sibling object and then we make a network call to destination server with stringified leaf
		right = n.right
		
		# correct left pointer of old next sibling to point to current new sibling
		if right['serverID'] != 'SXX':
			sib.right = right
			if right['serverID'] == myServerId:
				nextLeaf.readFromFile(right['fileName'])
				nextLeaf.left = sibling
				nextLeaf.printToFile(right['fileName'])
			else:
				# its left pointer to point to sibling.
				# correct sib.right to point to this
				query = 'CHANGELEFTPTR$' + right['fileName'] + '$' + sibling['serverID'] + '$' + sibling['fileName']
				response = client.request(right['serverID'], query)

		n.right = sibling
		sib.left = {'serverID': myServerId, 'fileName': fileName}
		# left/right things done. parent setting done below
		# If current leaf is root, handle separately. Happens in the beginning only once
		query = 'WHOISROOT'
		response = client.request(centralServerID, query)
		response = response.split('$')
		root = dict()
		root['serverID'] = response[0]
		root['fileName'] = response[1]

		if myServerId == root['serverID'] and fileName == root['fileName']: # this is root
			query = 'NEWNODE$' + str(midKey)
			response = client.request(centralServerID, query)
			response = response.split('$')
			root['serverID'] = response[0]
			root['fileName'] = response[1]
			# usual B+ Leaf split in case it is the root
			newRoot = self.Node()
			newRoot.key[0] = midKey
			newRoot.ptr[0] = {'serverID': myServerId, 'fileName': fileName}
			newRoot.ptr[1] = {'serverID': sibling['serverID'], 'fileName': sibling['fileName']}
			newRoot.keyCount = 1
			# save these info about root node
			# TODO : can save a network call here if same serverID
			query = 'SAVENODE$' + root['fileName'] + '$' + self.stringifyNode(newRoot)
			response = client.request(root['serverID'], query)
			# ask central server to change the root.
			query = 'CHANGEROOT$' + root['serverID'] + '$' + root['fileName']
			response = client.request(centralServerID, query)
			n.parent = root
			sib.parent = root
			n.printToFile(fileName)
			# print content to files
			if sibling['serverID'] == myServerId:
				sib.printToFile(sibling['fileName'])
			else:
				query = 'SAVELEAF$' + sibling['fileName'] + '$' + self.stringifyLeaf(sib)
				response = client.request(sibling['serverID'], query)
		else:
			# this leaf is not root
			sib.parent = n.parent
			n.printToFile(fileName)
			# print to files
			if sibling['serverID'] == myServerId:
				sib.printToFile(sibling['fileName'])
			else:
				query = 'SAVELEAF$' + sibling['fileName'] + '$' + self.stringifyLeaf(sib)
				response = client.request(sibling['serverID'], query)
				# network call to save sibling file in its host data server
				# now insert midKey | pointer in parent
				parent = n.parent
				if parent['serverID'] == myServerId:
					self.insertInNode(parent['fileName'], midKey, sibling)
				else:
					# make network call here
					query = 'INSERTINNODE$' + parent['fileName'] + '$' + str(midKey) + '$' + sibling['serverID'] + '$' + sibling['fileName']
					client.request(parent['serverID'], query)
		return 'SUCCESS'

	def saveLeaf(self, fileName, content):
		l = self.destringifyLeaf(content)
		l.printToFile(fileName)
		return 'SUCCESS'

	def saveNode(self, fileName, content):
		n = self.destringifyNode(content)
		n.printToFile(fileName)
		return 'SUCCESS'

	def changeLeftPtr(self, fileName, ptr):
		l = self.Leaf()
		l.readFromFile(fileName)
		l.left = ptr
		l.printToFile(fileName)
		return 'SUCCESS'
		
	def changeParent(self, fileName, ptr):
		if self.isLeaf(fileName):
			n = self.Leaf()
		else:
			n = self.Node()
		n.readFromFile(fileName)
		n.parent = ptr
		n.printToFile(fileName)
		return 'SUCCESS'

	def createLeaf(self, fileName):
		l = self.Leaf()
		l.printToFile(fileName)
		return 'SUCCESS'

	def createNode(self, fileName):
		n = self.Node()
		n.printToFile(fileName)
		return 'SUCCESS'

	def windowQuery1(self, fileName, left, right):
		l = self.Leaf()
		l.readFromFile(fileName)
		ans = []
		# possible optimization for Window2:
		# before starting to do anything, make network call to siblings
		start = 0
		while l.key[start] < left and start < l.keyCount:
			start += 1
		for i in range(start, l.keyCount):
			if l.key[i] < right:
				ans.append(l.key[i])
			else:
				return self.stringifyArray(ans)

		sibling = l.right
		query = 'WINDOWQUERY1$' + sibling['fileName'] + '$' + str(left) + '$' + str(right)
		# changing left won't make any difference
		if sibling['serverID'] != 'SXX':
			if sibling['serverID'] == myServerId:
				response = self.windowQuery1(sibling['fileName'], left, right)
			else:
				response = client.request(sibling['serverID'], query)
		else:
			response = ''

		if response != '': # do not merge with above if-else. response may also be '' if sibling has no such key 
			return self.stringifyArray(ans) + '$' + response
		else:
			return self.stringifyArray(ans)

	def knnQuery(self, fileName, center, k):
		l = self.Leaf()
		l.readFromFile(fileName)
		ans = []
		start = 0
		while l.key[start] < center and start < l.keyCount:
			start += 1

		for i in range(0, start):
			ans.append((abs(center-l.key[i]),l.key[i]))

		leftSibling = l.left
		remaining = k - len(ans)
		query = 'PREVKEYS$' + leftSibling['fileName'] + '$' + str(remaining)
		if remaining > 0 and leftSibling['serverID'] != 'SXX':
			if leftSibling['serverID'] == myServerId:
				leftKeys = self.prevKeys(leftSibling['fileName'], remaining)
			else:
				leftKeys = client.request(leftSibling['serverID'], query)
			leftKeys = leftKeys.split('$')
			for key in leftKeys:
				key = float(key)
				ans.append((abs(key-center), key))	

		rightCount = 0
		for i in range(start, l.keyCount):
			ans.append((abs(center-l.key[i]),l.key[i]))
			rightCount += 1

		remaining = k - rightCount
		rightSibling = l.right
		query = 'NEXTKEYS$' + rightSibling['fileName'] + '$' + str(remaining)

		if remaining > 0 and rightSibling['serverID'] != 'SXX':
			if rightSibling['serverID'] == myServerId:
				rightKeys = self.nextKeys(rightSibling['fileName'], remaining)
			else:
				rightKeys = client.request(rightSibling['serverID'], query)
			
			rightKeys = rightKeys.split('$')
			for key in rightKeys:
				key = float(key)
				ans.append((abs(key-center), key))

		ans = sorted(ans)
		final = []
		for key in ans:
			final.append(key[1])
		final =  final[0:k]
		return self.stringifyArray(final)

	def prevKeys(self, fileName, n):
		l = self.Leaf()
		l.readFromFile(fileName)
		ans = []
		
		for i in range(0, l.keyCount):
			ans.append(l.key[i])
		remaining = n - l.keyCount
		leftSibling = l.left
		query = 'PREVKEYS$' + leftSibling['fileName'] + '$' + str(remaining)
		
		if remaining > 0 and leftSibling['serverID'] != 'SXX':
			if leftSibling['serverID'] == myServerId:
				leftKeys = self.prevKeys(leftSibling['fileName'], remaining)
			else:
				leftKeys = client.request(leftSibling['serverID'], query)
			leftKeys = leftKeys.split('$')
			for key in leftKeys:
				key = float(key)
				ans.append(key)

		return self.stringifyArray(ans)


	def nextKeys(self, fileName, n):
		l = self.Leaf()
		l.readFromFile(fileName)
		ans = []
		
		for i in range(0, l.keyCount):
			ans.append(l.key[i])
		remaining = n - l.keyCount
		rightSibling = l.right
		query = 'NEXTKEYS$' + rightSibling['fileName'] + '$' + str(remaining)
		
		if remaining > 0 and rightSibling['serverID'] != 'SXX':
			if rightSibling['serverID'] == myServerId:
				rightKeys = self.nextKeys(rightSibling['fileName'], remaining)
			else:
				rightKeys = client.request(rightSibling['serverID'], query)
			rightKeys = rightKeys.split('$')
			for key in rightKeys:
				key = float(key)
				ans.append(key)

		return self.stringifyArray(ans)
