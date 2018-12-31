import os
from tqdm import tqdm
from DFD import genDFD
from diff_parser import parse_diff
import git

python_root_path = os.getcwd()


def filter(project_name):
    project_master_dir = python_root_path + "/" + project_name
    os.chdir(project_master_dir)
    output_dir = "../log/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    os.system("git log  --date=format:'%Y-%m-%d'  --pretty=format:\"%H%  %cd  %s\" > " + output_dir + "/master_log.txt")

    with open(output_dir + "/master_log.txt", encoding="utf-8") as fr:
        log_lines = fr.readlines()

    start = "df545a043386557f01fa75a1cd231b57688fa727"
    end = "4b316b984872b61f54aed26607df0d9d96326e9e"
    flag = False
    lines = []
    logs = []
    for line in log_lines:
        line = line.split()
        commit_id, date, log = line[0], line[1], " ".join(line[2:])
        if commit_id == start:
            flag = True
        if not flag:
            continue
        lines.append(commit_id)
        logs.append(log)
        if commit_id == end:
            flag = False

    return list(zip(lines, logs))


def DFD_continuous():
    project_name = "matplotlib"
    master_id = "e7719da6cad1d34c7a199833a822f4d2ec076ac8"
    os.chdir(python_root_path)
    os.chdir(project_name)
    os.system("git reset --hard {}".format(master_id))
    repo = git.Repo(python_root_path + '/' + project_name)
    filter_lines = filter(project_name)
    old_sha = master_id
    old_DFD = genDFD(python_root_path + '/' + project_name)
    changes = []
    for commit_id, log in tqdm(filter_lines):
        new_sha = commit_id
        os.system("git reset --hard --quiet {}".format(commit_id))
        new_DFD = genDFD(python_root_path + '/' + project_name)
        diff = repo.git.diff(new_sha, old_sha)
        cm_info=parse_diff(diff)
        cnt = 0
        for f in cm_info:
            filename = f.src_file
            if filename[-3:] != '.py':
                continue
            if filename in new_DFD.keys():
                for funcname, affected_new in new_DFD[filename].items():
                    if filename not in old_DFD.keys() or funcname not in old_DFD[filename].keys():
                        affected_old = set()
                    else:
                        affected_old = old_DFD[filename][funcname]
                    cnt += len(affected_new|affected_old) - len(affected_new&affected_old)
            if filename in old_DFD.keys():
                for funcname, affected_old in old_DFD[filename].items():
                    if filename not in new_DFD.keys() or funcname not in new_DFD[filename].keys():
                        affected_new = set()
                    else:
                        affected_new = new_DFD[filename][funcname]
                    cnt += len(affected_new|affected_old) - len(affected_new&affected_old)
        changes.append((new_sha, cnt, log))
        old_sha = new_sha
        old_DFD = new_DFD

    master_id = "e7719da6cad1d34c7a199833a822f4d2ec076ac8"
    os.chdir(python_root_path)
    os.chdir(project_name)
    os.system("git reset --hard {}".format(master_id))
    os.chdir(python_root_path)

    with open("output/result_continuous.txt", 'w', encoding = 'utf-8') as f:
        for change in changes:
            f.write(change[0]+ ' ' + str(change[1]) + ' ' + change[2] +"\n")

def DFD_func():
    project_name = "matplotlib"
    master_id = "e7719da6cad1d34c7a199833a822f4d2ec076ac8"
    os.chdir(python_root_path)
    os.chdir(project_name)
    os.system("git reset --hard {}".format(master_id))
    repo = git.Repo(python_root_path + '/' + project_name)
    old_sha = master_id
    old_DFD = genDFD(python_root_path + '/' + project_name)
    versions = {'v3.0.0': 'df545a043386557f01fa75a1cd231b57688fa727',
                'v2.2.3': '2e0eb748d3c1b808ed89e86e80a2d1565b4cd896',
                'v2.2.2': 'b471ee21cbe0d0fdd9cf5142d0a4be01517f4e68',
                'v2.2.1': '1021510fb4bf09680294255527ff07ce7fa3c527',
                'v2.2.0': '66e49f9a28f29b9a3a18cd4c6bfd5fdd1836eb0e',
                'v2.1.2': '24f0d9c47a00c2e58da421c0621eb2e90579e4c6',
                'v2.1.1': 'be7e4e46dc010bc237485081b42e541190754285',
                'v2.1.0': 'b392d46466e98cd6a437e16b52b3ed8de23b0b52',
                'v2.0.2': 'e175a41cb81880dbc553d9140e6ae5717457afa8',
                'v2.0.1': 'cef1be3e6e6cb9b0df403fa2869db4f9f75aff09',
                'v2.0.0': '1bfc7551f32f7b42ba50620a837f03e51d5b7c77'}

    changes = []
    for version, commit_id in tqdm(versions):
        new_sha = commit_id
        os.system("git reset --hard --quiet {}".format(commit_id))
        new_DFD = genDFD(python_root_path + '/' + project_name)
        diff = repo.git.diff(new_sha, old_sha)
        cm_info=parse_diff(diff)
        cnt = 0
        for f in cm_info:
            filename = f.src_file
            if filename[-3:] != '.py':
                continue
            if filename in new_DFD.keys():
                for funcname, affected_new in new_DFD[filename].items():
                    if filename not in old_DFD.keys() or funcname not in old_DFD[filename].keys():
                        affected_old = set()
                    else:
                        affected_old = old_DFD[filename][funcname]
                    cnt += len(affected_new|affected_old) - len(affected_new&affected_old)
            if filename in old_DFD.keys():
                for funcname, affected_old in old_DFD[filename].items():
                    if filename not in new_DFD.keys() or funcname not in new_DFD[filename].keys():
                        affected_new = set()
                    else:
                        affected_new = new_DFD[filename][funcname]
                    cnt += len(affected_new|affected_old) - len(affected_new&affected_old)
        changes.append((new_sha, cnt, version))
        old_sha = new_sha
        old_DFD = new_DFD

    master_id = "e7719da6cad1d34c7a199833a822f4d2ec076ac8"
    os.chdir(python_root_path)
    os.chdir(project_name)
    os.system("git reset --hard {}".format(master_id))
    os.chdir(python_root_path)

    with open("output/result_func.txt", 'w', encoding = 'utf-8') as f:
        for change in changes:
            f.write(change[2] + ' ' + change[0]+ ' ' + str(change[1]) + "\n")


if __name__ == '__main__':
    DFD_func()
    DFD_continuous()
