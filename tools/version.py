# This file generates versioned files for deploying Shabby

import yaclog
import yaclog.version
import git as gp
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


def run():
    basedir = Path(__file__).parent.parent

    repo = gp.Repo(basedir)
    cl = yaclog.Changelog('CHANGELOG.md')
    version = str(cl.current_version(released=True).version)
    release = False
    build = 0

    for tag in repo.tags:
        #todo: this should really be part of Yaclog's API
        if tag.commit == repo.head.commit:
            release = True
            build = 0
            break

    if not release:
        build = int.from_bytes(repo.head.commit.binsha[0:2], byteorder='big')
        version = yaclog.version.increment_version(version, 2)

    print(f'Configuring version {version} build {build}')

    ver_major, ver_minor, ver_patch = tuple(version.split('.'))

    env = Environment(
        loader=FileSystemLoader(basedir / "Templates"),
        autoescape=select_autoescape()
    )
    
    for template_name in ["Assets/Shabby.version", "Source/assembly/AssemblyInfo.cs"]:
        print("Generating " + template_name)
        template = env.get_template(template_name)
        with open(basedir / template_name, "w") as fh:
            fh.write(template.render(
                ver_major=ver_major,
                ver_minor=ver_minor,
                ver_patch=ver_patch,
                ver_build=build
            ))


    print('Done!')

if __name__ == '__main__':
    run()
