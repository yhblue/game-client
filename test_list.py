class person(object):
	"""docstring for person"""
	def __init__(self, name,x,y):
		self.name = name
		self.x = x
		self.y = y
	def tell_msg(self):
		print("name:"+self.name)
		print("x=%d"%self.x)	
		print("y=%d"%self.y)

def list_test():
	person_list = []
	a1 = person("jack",20,30)
	a2 = person("vivi",40,90)
	a3 = person("dayse",30,20)

	person_list.append(a1)
	person_list.append(a2)
	person_list.append(a3)

	print("member is %d"%len(person_list))
	for per in person_list:
		per.tell_msg()

if __name__ == "__main__":
	#main()
	list_test()