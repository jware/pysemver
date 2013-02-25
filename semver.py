import re


class SemVer(object):

    regex = re.compile(r'^(?P<major>[0-9]+)'
                       r'\.(?P<minor>[0-9]+)'
                       r'\.(?P<patch>[0-9]+)'
                       r'(\-(?P<prerelease>[0-9A-Za-z]+(\.[0-9A-Za-z]+)*))?'
                       r'(\+(?P<build>[0-9A-Za-z]+(\.[0-9A-Za-z]+)*))?$')

    # Core methods

    def __init__(self, version):
        if version == None:
            self.initialized = False
        else:
            self.parse(version)
            self.initialized = True

    def __bool__(self):
        return self.initialized

    def __gt__(self, other):
        if isinstance(other, SemVer):
            if self._compare(other) == 1:
                return True
            else:
                return False
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, SemVer):
            if self._compare(other) == -1:
                return True
            else:
                return False
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, SemVer):
            if self._compare(other) == 0:
                return True
            else:
                return False
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, SemVer):
            if self._compare(other) == 0 and self._compare(other) == 1:
                return True
            else:
                return False
        else:
            return NotImplemented

    def __le__(self, other):
        if isinstance(other, SemVer):
            if self._compare(other) == 0 and self._compare(other) == 1:
                return True
            else:
                return False
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, SemVer):
            if self._compare(other) == 1 or self._compare(other) == -1:
                return True
            else:
                return False
        else:
            return NotImplemented

    def __str__(self):
        temp_str = str(self.major) + "." + str(self.minor) + "." + str(self.patch)
        if self.prerelease != None:
            temp_str += "-" + str(self.prerelease)
        if self.build != None:
            temp_str += "+" + str(self.build)
        return temp_str

    def __iter__(self):
        if self.initialized == True:
            result = [self.major,
                    self.minor,
                    self.patch]
            if self.prerelease != None:
                result.append(self.prerelease)
            if self.build != None:
                result.append(self.build)
            return iter(result)
        else:
            return False

    # Utility functions

    @classmethod
    def valid(cls, version):
        if cls.regex.match(version):
            return True
        else:
            return False

    def parse(self, version):
        match = self.regex.match(version)

        if match is None:
            raise ValueError('%s is not valid SemVer string' % version)

        info = match.groupdict()

        self.major = int(info['major'])
        self.minor = int(info['minor'])
        self.patch = int(info['patch'])

        if info['prerelease'] != None:
            self.prerelease = info['prerelease']
        else:
            self.prerelease = None
        if info['build'] != None:
            self.build = info['build']
        else:
            self.build = None
        return True

    def _compare(self, other):
        i = 0
        for x1, x2 in zip(self, other):
            if i > 2:
                for y1, y2 in zip(x1.split('.'), x2.split('.')):
                    if y1.isnumeric():
                        y1 = int(y1)
                    if y2.isnumeric():
                        y2 = int(y2)
                    if y1 > y2:
                        return 1
                    elif y1 < y2:
                        return -1
            else:
                if x1 > x2:
                    return 1
                elif x1 < x2:
                    return -1
            i += 1
        return 0
