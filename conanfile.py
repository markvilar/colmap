from conans import ConanFile, CMake, tools

required_conan_version = ">=1.53.0"

class ColmapConanFile(ConanFile):
    name = "colmap"
    version = "3.9"
    license = "BSD"
    author = "Martin Kvisvik Larsen"
    description = "COLMAP - Structure-from-Motion and Multi-View Stereo"
    url = "https://github.com/markvilar/colmap"
    homepage = "https://colmap.github.io/"

    settings = ["os", "compiler", "build_type", "arch"]
    
    options = {
        "shared" : [True, False], 
        "fPIC" : [True, False]
    }
    
    default_options = {
        "shared" : False, 
        "fPIC" : True
    }

    exports_sources = [
        "CMakeLists.txt", 
        "cmake/*",
        "lib/*", 
        "scripts/*",
        "src/*", 
    ]
    
    generators = ["cmake_find_package", "cmake_find_package_multi"]

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        """ Configure project settings. """
        if self.options.shared:
            del self.options.fPIC
        # TODO: Set up configuration of dependencies
        # self.options["glad"].shared        = False
        # self.options["spdlog"].header_only = True

    def requirements(self):
        """ Specifies the requirements of the project. """
        self.requires("cmake/[>=3.17.0]")
        self.requires("boost/[1.70.0]") # TODO: Check req. version
        self.requires("ceres-solver/2.1.0")
        self.requires("eigen/3.4.0")
        self.requires("freeimage/3.18.0")
        self.requires("flann/1.9.2")
        self.requires("glew/2.2.0")
        self.requires("glog/0.6.0")
        self.requires("lz4/1.9.4")
        self.requires("metis/5.1.1")
        self.requires("opengl/system")
        self.requires("sqlite3/3.40.1")
        self.requires("qt/[>5.0.0 <5.18.0]")

        # Override dependency conflicts
        self.requires("openssl/1.1.1s")
        self.requires("zlib/[>=1.2.13]")
        self.requires("libpng/[>=1.6.37]")
        self.requires("libjpeg/9e")

    def validate(self):
        """ Validates the project configuration. """
        if self.settings.compiler == "clang":
            if tools.Version(self.settings.compiler.version) < "8":
                raise ConanInvalidConfiguration("Invalid clang compiler \
                    version.")
        if self.settings.compiler == "gcc":
            if tools.Version(self.settings.compiler.version) < "7":
                raise ConanInvalidConfiguration("Invalid gcc compiler \
                    version.")
        if self.settings.compiler == "Visual Studio":
            if tools.Version(self.settings.compiler.version) < "16":
                raise ConanInvalidConfiguration("Invalid Visual Studio \
                    compiler version.")

    def _configure_cmake(self):
        """ Internal method to configure CMake when Conan creates the 
        package."""
        cmake = CMake(self)
        # TODO: Look at definitions
        # cmake.definitions["PINE_BUILD_SHARED"] = self.options["shared"]
        # cmake.definitions["PINE_BUILD_WARNING"] = True
        cmake.configure(build_folder=self._build_subfolder)        
        return cmake

    def build(self):
        """ Builds the project. """
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        """ Packages the project. """
        self.copy("LICENSE*", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        """ Configures the package information. """
        # TODO: Clean up
        """
        # ImGui component
        self.cpp_info.components["libimgui"].libs = ["imgui"]
        self.cpp_info.components["libimgui"].requires = ["glfw::glfw"]
        """
        pass
