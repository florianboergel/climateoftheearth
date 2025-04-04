import numpy as np

class Planet:

    def __init__(self, configuration):

        self.resolution = configuration["resolution"]
        self.planetRadius = configuration["planetRadius"]      
        self.circumference = 2*np.pi*self.planetRadius
        self.circle = np.pi*self.planetRadius**2
        self.setupGrid(self.resolution)

        ### Properties of the planet
        self.nu = configuration["nu"]
        self.insolation = configuration["insolation"]
        self.epsilon = configuration["epsilon"]
        self.sigma = configuration["sigma"]
        self.airDensity = configuration["airDensity"]
        self.specificGasAir = configuration["specificGasAir"]
        self.heatCapacityEarth = configuration["heatCapacityEarth"]
        self.heatCapacityAtmosphere = configuration["heatCapacityAtmosphere"]
        self.thermalDiffusivityAir = configuration["thermalDiffusivityAir"]
        self.thermalDiffusivityOcean = configuration["thermalDiffusivityOcean"]
        self.coriolis = np.zeros((self.nlat, self.nlon))

        self.omega = 7.2921e-5
  

        for i in range(self.nlon):
            for j in range(self.nlat):
                # Standard Coriolis parameter for latitudes outside the threshold
                self.coriolis[j, i] = 2 * self.omega * np.sin(np.radians(self.lat[j]))

    def setupGrid(self, resolution):

        self.lat = np.arange(-90, 91, resolution)
        self.lon = np.arange(0, 361, resolution)
        self.nlat = len(self.lat)
        self.nlon = len(self.lon)
        self.dx = np.zeros((self.nlat, self.nlon))
        self.dy = np.zeros((self.nlat, self.nlon))
        for i in range(self.nlat):
            self.dx[i,:] = self.circumference/self.nlon*np.cos(self.lat[i]*np.pi/180)
        self.dy[:,:] = 0.5*self.circumference/(self.nlat-1)

        