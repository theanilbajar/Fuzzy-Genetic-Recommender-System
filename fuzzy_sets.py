class Age:
    def young(self, age):
        if age < 20.0:
            return 1.0
        elif age >= 20.0 and age < 35.0:
            return float((35-age)/15.0)
        else:
            return 0.0
        
    def middle(self, age):
        if age <= 20 or age > 60:
            return 0.0
        elif age > 20 and age <= 35:
            return (float(age-20)/15)
        elif age >35 and age <=45:
            return 1.0
        elif age > 45 and age <= 60:
            return ((60-age)/15.0)
        
    def old(self, age):
        if age <= 45:
            return 0.0
        elif age > 45 and age <= 60:
            return ((age-45.0)/15)
        else:
            return 1.0

class GIM:

	def very_bad(self, gim):
		if gim <= 1.0:
			return 1.0
		else:
			return 0.0

	def gim_a(self, gim, i):
		if gim <= i-2 or gim > i:
			return 0.0
		elif gim > i-2 and gim <= i-1:
			return (gim-i+2.0)
		elif gim > i-1 and gim <= i:
			return float(i-gim)
	
	def bad(self, gim):
		return self.gim_a(gim, 2.0)
	def average(self, gim):
		return self.gim_a(gim, 3.0)
	def good(self, gim):
		return self.gim_a(gim, 4.0)
	def very_good(self, gim):
		return self.gim_a(gim, 5.0)

	def excellent(self, gim):
		if gim <=4.0:
			return 0.0
		else:
			return (gim-4.0)
