import argparse
import sys

class Cli:
    @staticmethod
    def run():
        return Cli().execute()

    def execute(self):
        argparser = self._get_argparser()
        return argparser.parse_args(sys.argv[1:])

    def _get_argparser(self):
        argparser = argparse.ArgumentParser(sys.argv[0], description="mass repository deporter")
        argparser.add_argument("verb", type=str, help="verb of action = [migrate | mirror | transmigrate]")
        argparser.add_argument("-s", "--source", type=str, help="generic source node, expect a path to a configuration file [yml|json]")
        argparser.add_argument("-d", "--destination", type=str, help="generic destination node, expect a path to a configuration file [yml|json]")
        argparser.add_argument("-m", "--mirror", type=str, help="generic mirror node, expect a path to a configuration file [yml|json]")
        argparser.add_argument("-u", "--update-db", help="force DB update")
        return argparser
