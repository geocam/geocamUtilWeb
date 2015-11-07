#!/usr/bin/env python

"""
Check for secrets that should not be exposed in a public git repo,
across a number of repos in one go.

Your secrets file should have one secret per line. Your secret is
interpreted as a literal string to check for. Leading and trailing
whitespace is ignored. Comments and blank lines are ignored.  It would
be easy to expand the checker to use regexes for secrets, but it
currently does not.

If you find anything bad, you can use a tool like BFG Cleaner
https://rtyley.github.io/bfg-repo-cleaner/ to rewrite history and
expunge it before publishing.

"""

import sys
import tempfile
import subprocess
import getpass
import os


# should edit this to be the list of repos we plan to open source eventually
REPOS = (
    'https://babelfish.arc.nasa.gov/git/xgds_basalt',
    'https://babelfish.arc.nasa.gov/git/xgds_basalt_deploy',
    'https://babelfish.arc.nasa.gov/git/xgds_data',
    'https://babelfish.arc.nasa.gov/git/xgds_image',
    'https://babelfish.arc.nasa.gov/git/xgds_kn',
    'https://babelfish.arc.nasa.gov/git/xgds_planner2',
    'https://babelfish.arc.nasa.gov/git/xgds_plot',
    'https://babelfish.arc.nasa.gov/git/xgds_plrp',
    'https://babelfish.arc.nasa.gov/git/xgds_plrp_deploy',
    'https://babelfish.arc.nasa.gov/git/xgds_rp',
    'https://babelfish.arc.nasa.gov/git/xgds_rp_deploy',
    'https://babelfish.arc.nasa.gov/git/xgds_sample',
    'https://babelfish.arc.nasa.gov/git/xgds_video',
)


def dosys(cmd):
    print cmd
    ret = os.system(cmd)
    if ret != 0:
        print 'command exited with non-zero return value %s' % ret
    return ret


def dosysGetOutput(cmd, hidePattern):
    print cmd.replace(hidePattern, '<secret>')
    output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    return output


def checkRepoForSecrets(log, repoUrl, secrets):
    path = tempfile.mkdtemp(suffix='_checkForSecrets')
    oldDir = os.getcwd()
    os.chdir(path)
    dosys('pcache git clone %s' % repoUrl)
    repoDir = os.path.basename(repoUrl)
    repoDir = os.path.splitext(repoDir)[0]
    log.write('\n--REPO %s\n\n' % repoUrl)
    for i, secret in enumerate(secrets):
        log.write('--SECRET %s\n' % i)
        os.chdir(repoDir)
        output = dosysGetOutput('git rev-list --all | xargs git grep %s' % secret,
                                hidePattern=secret)
        os.chdir(path)
        log.write(output)
    os.chdir(oldDir)


def checkForSecrets(secretsPath):
    secrets = [secret.strip() for secret in open(secretsPath, 'r')]
    # ignore blank lines or comments in secrets file
    secrets = [secret for secret in secrets
               if secret != '' and not secret.startswith('#')]
    repos = REPOS
    logPath = 'checkForSecrets.log'
    with open(logPath, 'w') as log:
        print 'will check for secrets in these directories:'
        for repo in repos:
            print '  ', repo
        for repo in repos:
            checkRepoForSecrets(log, repo, secrets)
    print 'wrote results to %s' % logPath


def main():
    import optparse
    parser = optparse.OptionParser('usage: %prog <secrets_file.txt>\n' + __doc__ + '\n')
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error('expected exactly 1 arg')
    secretsPath = args[0]
    checkForSecrets(secretsPath)
    print('you should be able to clean up temp files by running a command like this: rm -rf /tmp/*_checkForSecrets (may vary a bit based on operating system)')


if __name__ == '__main__':
    main()
