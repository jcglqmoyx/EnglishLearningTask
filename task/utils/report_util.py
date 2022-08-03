from task.utils.datetime_util import get_date_str


def generate_report(group_id, successful_members, rest_for_one_day_members, rest_for_two_days_members, failed_members):
    def output_records(members):
        s = ''
        for member, records in members.items():
            if not records:
                s += '%s\n' % member
                continue
            s += '%s ' % member
            for i in range(len(records)):
                s += '[链接%d](%s) ' % (i + 1, records[i].image_url)
            s += '<br>'
        s += '\n'
        return s

    date_str = get_date_str()
    f = open('./task/templates/markdown/%s_%d.md' % (date_str, group_id), 'w')
    f.write('# %s %d群 打卡情况\n' % (date_str, group_id))

    f.write('## 完成打卡的朋友\n')
    if successful_members:
        f.write(output_records(successful_members))

    if rest_for_one_day_members:
        f.write('## 选择休息一天的朋友\n')
        f.write(output_records(rest_for_one_day_members))

    if rest_for_two_days_members:
        f.write('## 选择休息两天的朋友\n')
        f.write(output_records(rest_for_two_days_members))

    if failed_members:
        f.write('## 未完成打卡的朋友\n')
        f.write(output_records(failed_members))

    f.close()
