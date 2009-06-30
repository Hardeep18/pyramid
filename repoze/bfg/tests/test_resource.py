import unittest
from repoze.bfg.testing import cleanUp

class TestOverrideProvider(unittest.TestCase):
    def setUp(self):
        cleanUp()

    def tearDown(self):
        cleanUp()

    def _getTargetClass(self):
        from repoze.bfg.resource import OverrideProvider
        return OverrideProvider

    def _makeOne(self, module):
        klass = self._getTargetClass()
        return klass(module)

    def _registerOverrides(self, overrides, name='repoze.bfg.tests'):
        from repoze.bfg.interfaces import IPackageOverrides
        from zope.component import getSiteManager
        sm = getSiteManager()
        sm.registerUtility(overrides, IPackageOverrides, name=name)

    def test_get_resource_filename_no_overrides(self):
        import os
        resource_name = 'test_resource.py'
        import repoze.bfg.tests
        provider = self._makeOne(repoze.bfg.tests)
        here = os.path.dirname(os.path.abspath(__file__))
        expected = os.path.join(here, resource_name)
        result = provider.get_resource_filename(None, resource_name)
        self.assertEqual(result, expected)

    def test_get_resource_stream_no_overrides(self):
        import os
        resource_name = 'test_resource.py'
        import repoze.bfg.tests
        provider = self._makeOne(repoze.bfg.tests)
        here = os.path.dirname(os.path.abspath(__file__))
        expected = open(os.path.join(here, resource_name)).read()
        result = provider.get_resource_stream(None, resource_name)
        self.assertEqual(result.read(), expected)

    def test_get_resource_string_no_overrides(self):
        import os
        resource_name = 'test_resource.py'
        import repoze.bfg.tests
        provider = self._makeOne(repoze.bfg.tests)
        here = os.path.dirname(os.path.abspath(__file__))
        expected = open(os.path.join(here, resource_name)).read()
        result = provider.get_resource_string(None, resource_name)
        self.assertEqual(result, expected)

    def test_get_resource_filename_override_returns_None(self):
        overrides = DummyOverrides(None)
        self._registerOverrides(overrides)
        import os
        resource_name = 'test_resource.py'
        import repoze.bfg.tests
        provider = self._makeOne(repoze.bfg.tests)
        here = os.path.dirname(os.path.abspath(__file__))
        expected = os.path.join(here, resource_name)
        result = provider.get_resource_filename(None, resource_name)
        self.assertEqual(result, expected)
        
    def test_get_resource_stream_override_returns_None(self):
        overrides = DummyOverrides(None)
        self._registerOverrides(overrides)
        import os
        resource_name = 'test_resource.py'
        import repoze.bfg.tests
        provider = self._makeOne(repoze.bfg.tests)
        here = os.path.dirname(os.path.abspath(__file__))
        expected = os.path.join(here, resource_name)
        result = provider.get_resource_filename(None, resource_name)
        self.assertEqual(result, expected)

    def test_get_resource_string_override_returns_None(self):
        overrides = DummyOverrides(None)
        self._registerOverrides(overrides)
        import os
        resource_name = 'test_resource.py'
        import repoze.bfg.tests
        provider = self._makeOne(repoze.bfg.tests)
        here = os.path.dirname(os.path.abspath(__file__))
        expected = os.path.join(here, resource_name)
        result = provider.get_resource_filename(None, resource_name)
        self.assertEqual(result, expected)

    def test_get_resource_filename_override_returns_value(self):
        overrides = DummyOverrides('value')
        import repoze.bfg.tests
        self._registerOverrides(overrides)
        provider = self._makeOne(repoze.bfg.tests)
        result = provider.get_resource_filename(None, 'test_resource.py')
        self.assertEqual(result, 'value')

    def test_get_resource_stream_override_returns_value(self):
        overrides = DummyOverrides('value')
        import repoze.bfg.tests
        self._registerOverrides(overrides)
        provider = self._makeOne(repoze.bfg.tests)
        result = provider.get_resource_stream(None, 'test_resource.py')
        self.assertEqual(result, 'value')

    def test_get_resource_string_override_returns_value(self):
        overrides = DummyOverrides('value')
        import repoze.bfg.tests
        self._registerOverrides(overrides)
        provider = self._makeOne(repoze.bfg.tests)
        result = provider.get_resource_string(None, 'test_resource.py')
        self.assertEqual(result, 'value')

class TestPackageOverrides(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.bfg.resource import PackageOverrides
        return PackageOverrides

    def _makeOne(self, package, pkg_resources=None):
        klass = self._getTargetClass()
        if pkg_resources is None:
            pkg_resources = DummyPkgResources()
        return klass(package, pkg_resources=pkg_resources)

    def test_ctor_package_already_has_loader(self):
        package = DummyPackage('package')
        package.__loader__ = True
        self.assertRaises(TypeError, self._makeOne, package)

    def test_ctor_sets_loader(self):
        package = DummyPackage('package')
        po = self._makeOne(package)
        self.assertEqual(package.__loader__, po)

    def test_ctor_registers_loader_type(self):
        from repoze.bfg.resource import OverrideProvider
        dummy_pkg_resources = DummyPkgResources()
        package = DummyPackage('package')
        po = self._makeOne(package, dummy_pkg_resources)
        self.assertEqual(dummy_pkg_resources.registered, [(po.__class__,
                         OverrideProvider)])

    def test_ctor_sets_local_state(self):
        package = DummyPackage('package')
        po = self._makeOne(package)
        self.assertEqual(po.overrides, [])
        self.assertEqual(po.overridden_package_name, 'package')

    def test_insert_directory(self):
        from repoze.bfg.resource import DirectoryOverride
        package = DummyPackage('package')
        po = self._makeOne(package)
        po.overrides= [None]
        po.insert('foo/', 'package', 'bar/')
        self.assertEqual(len(po.overrides), 2)
        override = po.overrides[0]
        self.assertEqual(override.__class__, DirectoryOverride)

    def test_insert_file(self):
        from repoze.bfg.resource import FileOverride
        package = DummyPackage('package')
        po = self._makeOne(package)
        po.overrides= [None]
        po.insert('foo.pt', 'package', 'bar.pt')
        self.assertEqual(len(po.overrides), 2)
        override = po.overrides[0]
        self.assertEqual(override.__class__, FileOverride)

    def test_search_path(self):
        overrides = [ DummyOverride(None), DummyOverride(('package', 'name'))]
        package = DummyPackage('package')
        po = self._makeOne(package)
        po.overrides= overrides
        self.assertEqual(list(po.search_path('whatever')),
                         [('package', 'name')])

    def test_get_filename(self):
        import os
        overrides = [ DummyOverride(None), DummyOverride(
            ('repoze.bfg.tests', 'test_resource.py'))]
        package = DummyPackage('package')
        po = self._makeOne(package)
        po.overrides= overrides
        here = os.path.dirname(os.path.abspath(__file__))
        expected = os.path.join(here, 'test_resource.py')
        self.assertEqual(po.get_filename('whatever'), expected)
        
    def test_get_stream(self):
        import os
        overrides = [ DummyOverride(None), DummyOverride(
            ('repoze.bfg.tests', 'test_resource.py'))]
        package = DummyPackage('package')
        po = self._makeOne(package)
        po.overrides= overrides
        here = os.path.dirname(os.path.abspath(__file__))
        expected = open(os.path.join(here, 'test_resource.py')).read()
        self.assertEqual(po.get_stream('whatever').read(), expected)
        
    def test_get_string(self):
        import os
        overrides = [ DummyOverride(None), DummyOverride(
            ('repoze.bfg.tests', 'test_resource.py'))]
        package = DummyPackage('package')
        po = self._makeOne(package)
        po.overrides= overrides
        here = os.path.dirname(os.path.abspath(__file__))
        expected = open(os.path.join(here, 'test_resource.py')).read()
        self.assertEqual(po.get_string('whatever'), expected)
        

class TestDirectoryOverride(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.bfg.resource import DirectoryOverride
        return DirectoryOverride

    def _makeOne(self, path, package, prefix):
        klass = self._getTargetClass()
        return klass(path, package, prefix)

    def test_it_match(self):
        o = self._makeOne('foo/', 'package', 'bar/')
        result = o('foo/something.pt')
        self.assertEqual(result, ('package', 'bar/something.pt'))
        
    def test_it_no_match(self):
        o = self._makeOne('foo/', 'package', 'bar/')
        result = o('baz/notfound.pt')
        self.assertEqual(result, None)
        

class TestFileOverride(unittest.TestCase):
    def _getTargetClass(self):
        from repoze.bfg.resource import FileOverride
        return FileOverride

    def _makeOne(self, path, package, prefix):
        klass = self._getTargetClass()
        return klass(path, package, prefix)

    def test_it_match(self):
        o = self._makeOne('foo.pt', 'package', 'bar.pt')
        result = o('foo.pt')
        self.assertEqual(result, ('package', 'bar.pt'))
        
    def test_it_no_match(self):
        o = self._makeOne('foo.pt', 'package', 'bar.pt')
        result = o('notfound.pt')
        self.assertEqual(result, None)
        
class DummyOverride:
    def __init__(self, result):
        self.result = result

    def __call__(self, resource_name):
        return self.result

class DummyOverrides:
    def __init__(self, result):
        self.result = result

    def get_filename(self, resource_name):
        return self.result

    get_stream = get_string = get_filename
    
class DummyPkgResources:
    def __init__(self):
        self.registered = []

    def register_loader_type(self, typ, inst):
        self.registered.append((typ, inst))
        
class DummyPackage:
    def __init__(self, name):
        self.__name__ = name
    
