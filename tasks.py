import gym
import h5py
import numpy as np
import matplotlib.pylab as plt
import random

"""
This function stores to a file the frame generated by the openai-gym environment specified with env
env : environment
episodes : Number of games to store. A game is completed when the environment return's done as true in env.step
policy : This should be a function that takes as input the frame and outputs an action. For a random policy the input is not 
used but should be declared nonetheless
filename: Name of the filename where is going to be stored the data
colorM	
"""
def gatherData(env, episodes, policy, filename, colorMode = 'gray'):

	f = filename

	for episode in range(episodes):
		env.reset()	

		episodeNumber = f.create_group("episode" + str(episode))
		#iterations = episodeNumber.create_dataset("iteration" + str(episode), (episodes, ), maxshape = (None, ))
		iterations = []
		#images = episodeNumber.create_dataset("image" + str(episode), (episodes, 4), maxshape = (None, 4))
		#rewards = episodeNumber.create_dataset("reward" + str(episode), (episodes, ), maxshape = (None, ))
		#finished = episodeNumber.create_dataset("finished" + str(episode), (episodes, ), maxshape = (None, ), dtype = bool)
		images = []
		rewards = []
		finished = []
		i = 0

		while (True):
			env.render()

			randomAction = env.action_space.sample()
			observation, reward, done, info = env.step(randomAction)
			iterations.append(i)
			#images[i] = observation
			#rewards[i] = reward
			#finished[i] = done
			images.append(observation)
			rewards.append(reward)
			finished.append(done)

			i = i + 1

			#Resets if done
			if (done):
				i = 0
				iters = episodeNumber.create_dataset("iteration" + str(episode), data = iterations)
				im = episodeNumber.create_dataset("image" + str(episode), data = images)
				rew = episodeNumber.create_dataset("reward" + str(episode), data = rewards)
				fin = episodeNumber.create_dataset("finished" + str(episode), data = finished)
				break	

"""
Add code for reading back the data from an specific episode and even visualize at random a small subset of the images. 
Create a function for reading the data and another for testing and visualizing the data. 
The test can be just to print on screen data size as you already have for the data storage part but from the loaded data. 
Basically create a function that loads the data into memory and another to visualize specified number of random frames 
and the size of the datasets. 
"""
def readData(filename, episode):
	#Only reads and returns observations right now
	f = filename

	episodeName = "/episode" + str(episode)
	imageName = episodeName + '/image' + str(episode)
	ep = f.get(episodeName)
	image = ep.get(imageName)
	return np.array(image)
			
def testAndVisualizeData(filename, episode, numImages):
	f = filename
	images = readData(filename, episode)
	print(len(images))
	#imageSubset = random.sample(range(0,))
	imageSample = []
	try: 
		imageSampleIndices = random.sample(range(0,len(images)),numImages)
	except ValueError:
		print("Your image subset is too big! Try a smaller number.")
		return

	for index in imageSampleIndices:
		imageSample.append(images[index])

	imageSample = np.array(imageSample)
	plt.imshow(imageSample)
	plt.show()

######################
##TESTS
######################

def testGatherData():
	testEnv = gym.make('CartPole-v0')
	episodes = 5
	dummyPolicy = ""
	testFile = h5py.File("test.hdf5", "w")
	gatherData(testEnv, episodes, dummyPolicy, testFile, 'gray')
	for val in testFile.values():
		print(val.name)
		for dset in val.values():
			print(dset.name)
			for i in range(len(dset)):
				print dset[i],
			print("")
		print("")

	print("")

def testReadData():
	testFile = h5py.File("test.hdf5", "a")
	readData(testFile, 0)

def testTestAndVisualizeData():
	testFile = h5py.File("test.hdf5", "a")
	testAndVisualizeData(testFile, 0, 5)

def testAll():
	#testGatherData()
	testReadData()
	testTestAndVisualizeData()

if __name__ == "__main__":
	testAll()


