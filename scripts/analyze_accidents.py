# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
from collections import defaultdict, Counter

# Read file
with open(r'c:\Users\chloe.chang\Documents\claude\職安\參考資料\公司職災資料\職災統計_v2_output.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse rows
records = []
for line in content.split('\n'):
    m = re.match(r'.*Row(\d+):\s*(.*)', line)
    if m:
        row_num = int(m.group(1))
        if row_num < 2:
            continue
        fields = m.group(2).split(' | ')
        if len(fields) >= 10:
            date_str = fields[0].strip()
            location = fields[1].strip()
            acc_class = fields[2].strip()
            acc_type = fields[3].strip()
            dept = fields[4].strip()
            fix_date = fields[5].strip()
            name = fields[6].strip()
            emp_id = fields[7].strip()
            rest_days_str = fields[8].strip()
            desc = fields[9].strip() if len(fields) > 9 else ''

            try:
                rest_days = float(rest_days_str)
            except:
                rest_days = 0

            try:
                dt = datetime.strptime(date_str, '%Y%m%d')
            except:
                dt = None

            records.append({
                'row': row_num,
                'date_str': date_str,
                'date': dt,
                'location': location,
                'acc_class': acc_class,
                'acc_type': acc_type,
                'dept': dept,
                'name': name,
                'emp_id': emp_id,
                'rest_days': rest_days,
                'desc': desc
            })

print(f"=== 1. Basic Stats ===")
print(f"Total records: {len(records)}")

dates = [r['date'] for r in records if r['date']]
dates_sorted = sorted(dates)
print(f"Date range: {dates_sorted[0].strftime('%Y/%m/%d')} ~ {dates_sorted[-1].strftime('%Y/%m/%d')}")

year_counts = Counter()
year_rest = defaultdict(float)
for r in records:
    if r['date']:
        y = r['date'].year
        year_counts[y] += 1
        year_rest[y] += r['rest_days']

for y in sorted(year_counts.keys()):
    print(f"  {y}: {year_counts[y]} 件")

total_rest = sum(r['rest_days'] for r in records)
print(f"Total lost workdays: {total_rest}")
for y in sorted(year_rest.keys()):
    print(f"  {y} lost days: {year_rest[y]}")

print()
print(f"=== 2. Weather Analysis ===")
weather_kw = ['雨', '濕滑', '積水', '炎熱', '高溫', '風勢']
weather_records = []
for r in records:
    matched_kw = []
    for kw in weather_kw:
        if kw in r['desc']:
            matched_kw.append(kw)
    if matched_kw:
        weather_records.append((r, matched_kw))

print(f"Weather-related records: {len(weather_records)}")
weather_rest_total = 0
for wr, kws in weather_records:
    weather_rest_total += wr['rest_days']
    print(f"  Row{wr['row']}: {wr['date_str']} | {wr['name']} | keywords: {','.join(kws)} | rest: {wr['rest_days']} | loc: {wr['location'][:40]}")

print(f"Weather total rest days: {weather_rest_total}")
non_weather_count = len(records) - len(weather_records)
non_weather_rest = total_rest - weather_rest_total
if weather_records:
    print(f"Weather avg rest: {weather_rest_total/len(weather_records):.2f}")
print(f"Non-weather avg rest: {non_weather_rest/non_weather_count:.2f}")

print()
print(f"=== 3. Work Type Classification ===")

def classify_work_type(r):
    loc = r['location']
    desc = r['desc']
    acc_type = r['acc_type']
    acc_class = r['acc_class']

    if '上下班' in acc_type:
        return '通勤'

    if acc_class == '交通事故' and '上下班' not in acc_type:
        return '駕駛運輸'

    customer_names = ['台積電', '矽品', '燿華', '日月光', '美光', '碼氏', '金成毅', '裕隆', '中國醫', '富聯', '華東科技', '晶傑達', '啟碁']
    for cn in customer_names:
        if cn in loc or cn in desc:
            return '客戶端作業'

    if any(kw in loc for kw in ['分選', '綜合貨', '細分選', '紙線', '玻璃']):
        return '廠內分選'

    if any(kw in loc for kw in ['造粒', '處理', '粉碎', '螺桿', '解包機']):
        return '製程操作'
    if any(kw in desc for kw in ['造粒機', '粉碎', '螺桿', '解包機']):
        return '製程操作'

    station_patterns = ['竹北站', '草屯站', '和美站', '神岡站', '新竹站', '安定倉', '沙鹿倉', '神岡倉', '中一倉', '中三倉']
    for sp in station_patterns:
        if sp in loc:
            return '站點/倉儲'

    if any(kw in desc for kw in ['覆網', '上下車', '下貨', '搬運', '出貨', '上貨', '卸貨']):
        return '裝卸搬運'

    return '其他'

work_type_counts = Counter()
work_type_rest = defaultdict(float)
work_type_records = defaultdict(list)
for r in records:
    wt = classify_work_type(r)
    r['work_type'] = wt
    work_type_counts[wt] += 1
    work_type_rest[wt] += r['rest_days']
    work_type_records[wt].append(r)

for wt in ['通勤', '駕駛運輸', '客戶端作業', '廠內分選', '製程操作', '站點/倉儲', '裝卸搬運', '其他']:
    cnt = work_type_counts[wt]
    avg = work_type_rest[wt]/cnt if cnt else 0
    print(f"  {wt}: {cnt} 件, total rest: {work_type_rest[wt]}, avg rest: {avg:.2f}")
    rows = [str(r['row']) for r in work_type_records[wt]]
    print(f"    Rows: {', '.join(rows)}")

print()
print(f"=== 4. Business Line Classification ===")

def classify_business(dept):
    if re.search(r'北區業務.*課', dept) or re.search(r'中區業務.*課', dept) or re.search(r'南區業務.*課', dept) or dept == '北一課' or dept == '五股分選課' or dept == '業務部專案管理課' or dept == '業務開發部' or dept.startswith('業務北區') or dept == '北三課' or dept == '企業客服課' or dept == '全興營業課':
        return '回收業務'

    if re.search(r'全興.*課', dept) or re.search(r'宏偉.*課', dept) or dept == '品保課' or dept == '再生處理部':
        return '再生處理'

    if re.search(r'.+站$', dept):
        return '站點營運'

    if dept in ['家電回收課', '廢車客服課', '拆解觀光課', '拆除工程課'] or dept.startswith('豐動'):
        return '家電/廢車'

    if dept.startswith('人資') or dept.startswith('法務') or dept in ['會計課', '財務課']:
        return '行政管理'

    return '其他'

biz_counts = Counter()
biz_dept_detail = defaultdict(lambda: Counter())
biz_records = defaultdict(list)
for r in records:
    biz = classify_business(r['dept'])
    biz_counts[biz] += 1
    biz_dept_detail[biz][r['dept']] += 1
    biz_records[biz].append(r)

for biz in ['回收業務', '再生處理', '站點營運', '家電/廢車', '行政管理', '其他']:
    print(f"  {biz}: {biz_counts[biz]} 件")
    if biz_dept_detail[biz]:
        for dept, cnt in sorted(biz_dept_detail[biz].items(), key=lambda x: -x[1]):
            print(f"    {dept}: {cnt}")

print()
print(f"=== 5. Day-of-Week Analysis ===")
dow_counts = Counter()
dow_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
for r in records:
    if r['date']:
        dow = r['date'].weekday()
        dow_counts[dow] += 1

for i in range(7):
    print(f"  {dow_names[i]}: {dow_counts[i]}")

print()
print(f"=== 6. Monthly Distribution ===")
month_counts = Counter()
for r in records:
    if r['date']:
        month_counts[r['date'].month] += 1
for m in range(1, 13):
    print(f"  {m}月: {month_counts[m]}")

print()
print(f"=== 7. Quarterly Distribution ===")
q_counts = Counter()
for r in records:
    if r['date']:
        q = (r['date'].month - 1) // 3 + 1
        q_counts[q] += 1
for q in range(1, 5):
    print(f"  Q{q}: {q_counts[q]}")

print()
print(f"=== 8. Geographic Analysis ===")

def classify_region(r):
    loc = r['location']
    desc = r['desc']
    combined = loc + ' ' + desc

    if any(kw in combined for kw in ['國道', '國一', '國二', '國三', '國四', '國八', '交流道', '國1', '國2', '國3', '國4', '台74']):
        return '國道/快速道路'

    north_kw = ['台北', '新北', '桃園', '新竹', '五股', '竹北', '土城', '湖口', '中壢', '龍潭', '竹南', '頭份', '宜蘭', '淡水', '新莊', '成泰路', '寶山']
    for kw in north_kw:
        if kw in loc:
            return '北區'

    south_kw = ['台南', '高雄', '嘉義', '永康', '新市', '安定', '安南', '西港', '前鎮']
    for kw in south_kw:
        if kw in loc:
            return '南區'

    mid_kw = ['台中', '彰化', '南投', '苗栗', '全興', '沙鹿', '和美', '神岡', '大里', '豐原', '后里', '草屯', '大雅', '伸港', '彰濱', '北屯', '宏偉', '雅潭', '總部']
    for kw in mid_kw:
        if kw in loc:
            return '中區'

    if '北區' in r['dept'] or '五股' in r['dept'] or '竹北' in r['dept'] or '新竹' in r['dept'] or '北一' in r['dept'] or '北三' in r['dept']:
        return '北區'
    if '南區' in r['dept']:
        return '南區'
    if '中區' in r['dept'] or '全興' in r['dept'] or '和美' in r['dept'] or '神岡' in r['dept'] or '草屯' in r['dept'] or '宏偉' in r['dept']:
        return '中區'

    return '其他/不明'

region_counts = Counter()
region_records = defaultdict(list)
for r in records:
    reg = classify_region(r)
    region_counts[reg] += 1
    region_records[reg].append(r)

for reg in ['中區', '北區', '南區', '國道/快速道路', '其他/不明']:
    print(f"  {reg}: {region_counts[reg]}")

if region_records['其他/不明']:
    print(f"  其他/不明 details:")
    for r in region_records['其他/不明']:
        print(f"    Row{r['row']}: {r['location'][:50]} | {r['dept']}")

print()
print(f"=== 9. Accident Density ===")
sorted_records = sorted([r for r in records if r['date']], key=lambda x: x['date'])
intervals = []
for i in range(1, len(sorted_records)):
    delta = (sorted_records[i]['date'] - sorted_records[i-1]['date']).days
    intervals.append((delta, sorted_records[i-1], sorted_records[i]))

avg_interval = sum(i[0] for i in intervals) / len(intervals)
print(f"Average interval: {avg_interval:.2f} days")

max_interval = max(intervals, key=lambda x: x[0])
print(f"Max interval (longest safe period): {max_interval[0]} days")
print(f"  From: {max_interval[1]['date'].strftime('%Y/%m/%d')} (Row{max_interval[1]['row']})")
print(f"  To: {max_interval[2]['date'].strftime('%Y/%m/%d')} (Row{max_interval[2]['row']})")

min_interval = min(intervals, key=lambda x: x[0])
print(f"Min interval: {min_interval[0]} days")

date_counts = Counter()
for r in records:
    if r['date']:
        date_counts[r['date'].strftime('%Y/%m/%d')] += 1
same_day = {d: c for d, c in date_counts.items() if c >= 2}
print(f"\nSame-day multiple events: {len(same_day)} days")
for d, c in sorted(same_day.items()):
    names = [r['name'] for r in records if r['date'] and r['date'].strftime('%Y/%m/%d') == d]
    print(f"  {d}: {c} events - {', '.join(names)}")

print(f"\nClusters (3+ events in 7 days):")
seen_clusters = set()
for i in range(len(sorted_records)):
    window_end = sorted_records[i]['date'] + timedelta(days=7)
    cluster = [sorted_records[i]]
    for j in range(i+1, len(sorted_records)):
        if sorted_records[j]['date'] <= window_end:
            cluster.append(sorted_records[j])
        else:
            break
    if len(cluster) >= 3:
        start = cluster[0]['date'].strftime('%Y/%m/%d')
        end = cluster[-1]['date'].strftime('%Y/%m/%d')
        key = f"{start}-{end}-{len(cluster)}"
        if key not in seen_clusters:
            seen_clusters.add(key)
            names = [f"{c['name']}({c['date'].strftime('%m/%d')})" for c in cluster]
            print(f"  {start} ~ {end}: {len(cluster)} events")
            print(f"    {', '.join(names)}")

print()
print(f"=== 10. Seasonal Analysis ===")
season_counts = Counter()
for r in records:
    if r['date']:
        m = r['date'].month
        if m in [3, 4, 5]:
            season_counts['春季(3-5月)'] += 1
        elif m in [6, 7, 8]:
            season_counts['夏季(6-8月)'] += 1
        elif m in [9, 10, 11]:
            season_counts['秋季(9-11月)'] += 1
        else:
            season_counts['冬季(12-2月)'] += 1

for s in ['春季(3-5月)', '夏季(6-8月)', '秋季(9-11月)', '冬季(12-2月)']:
    print(f"  {s}: {season_counts[s]}")

print()
print(f"=== 11. Repeat Offenders ===")
name_counts = Counter()
for r in records:
    name_counts[r['name']] += 1

repeaters = {n: c for n, c in name_counts.items() if c >= 2}
for n, c in sorted(repeaters.items(), key=lambda x: -x[1]):
    rows = [f"Row{r['row']}({r['date_str']})" for r in records if r['name'] == n]
    print(f"  {n}: {c} 次 - {', '.join(rows)}")
