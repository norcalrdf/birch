import math
import mmap

class BlockFile:
    @classmethod
    def open(cls, path, mode, block_size = 4096, growth_factor = 1.5):
        """mode - r, w, or rw."""
        self = cls()
        self.block_size = block_size
        self.growth_factor = growth_factor
        self.mode = mode
        self.path = path
        f = open(path, mode + 'b')
        if mode == 'r':
            access = mmap.PROT_WRITE
        else:
            access = mmap.PROT_READ | mmap.PROT_WRITE
        self.mmap = mmap.mmap(f.fileno(), length = 0, access = access)
    
    def close(self):
        self.mmap.close()
        del self.mmap
        del self.path

    def get_block(self, index):
        return self.mmap[index * self.block_size : (index+1) * self.block_size]

    def store_block(self, index, block):
        self.mmap[index * self.block_size : (index + 1) * self.block_size] = block
    
    def grow(self):
        new_size = int(math.floor(self.count() * self.growth_factor * self.block_size))
        self.mmap.resize(new_size)
    
    def count(self):
        return self.mmap.size() / self.block_size
