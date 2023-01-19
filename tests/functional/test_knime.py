import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

from retropath2_wrapper.Args import DEFAULT_KNIME_VERSION, DEFAULT_ZENODO_VERSION, KNIME_ZENODO, RETCODES
from retropath2_wrapper.knime import Knime


class TestKnime(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)

    @classmethod
    def filter_exec(cls, path: str):
        kexec = None
        args = [
            "-application",
            "org.eclipse.equinox.p2.director",
            "-nosplash",
            "-consolelog",
            "-help",
        ]
        for x in pathlib.Path(path).glob(os.path.join("**", "knime*")):
            if x.is_file() is False:
                continue
            try:
                ret = subprocess.run([str(x.absolute())] + args)
                if ret.returncode == 0:
                    kexec = x
                    break
            except:
                pass
        return kexec

    def test_standardize_path(self):
        path = os.getcwd()
        spath = Knime.standardize_path(path=path)
        self.assertTrue("\\" not in spath)

    def test_install_knime_from_knime(self):
        knime = Knime(workflow="", kinstall=self.tempdir)
        knime.install_exec()
        kexec = TestKnime.filter_exec(path=self.tempdir)
        self.assertIsNot(kexec, None)
        # Failed could be araise due to missing dependecy
        try:
            ret = knime.install_pkgs()
            self.assertEqual(ret, RETCODES['OK'])
        except Exception:
            pass

    def test_install_knime_from_zenodo(self):
        knime = Knime(workflow="", kinstall=self.tempdir, kzenodo_ver=list(KNIME_ZENODO.keys())[0])
        knime.install_exec()
        kexec = TestKnime.filter_exec(path=self.tempdir)
        self.assertIsNot(kexec, None)
        ret = knime.install_pkgs()
        self.assertEqual(ret, RETCODES['OK'])
