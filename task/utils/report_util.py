from task.utils.datetime_util import get_date_str


def generate_report(competent_members, incompetent_members):
    def output_records(members):
        s = ''
        for member, records in members.items():
            if not records:
                s += '%s\n' % member
                continue
            s += '%s ' % member
            for i in range(len(records)):
                s += '[链接%d](%s) ' % (i + 1, records[i].image_url)
        s += '\n'
        return s

    date_str = get_date_str()
    f = open('./%s.md' % date_str, 'w')
    f.write('# %s打卡情况\n' % date_str)
    f.write('## 完成打卡的朋友\n')
    if competent_members:
        f.write(output_records(competent_members))
    f.write('## 未完成打卡的朋友\n')
    if incompetent_members:
        f.write(output_records(incompetent_members))
    f.close()
