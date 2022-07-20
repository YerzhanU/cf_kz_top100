#!/usr/bin/env python3
import time

from codeforces import CodeforcesAPI


def get_all_user_handles(ranklist_rows):
    return set(m.handle for row in ranklist_rows for m in row.party.members)


def filter_by_organization(ranklist_row, handle_to_user_mapping, organization):
    return (r for r in ranklist_row if handle_to_user_mapping[r.party.members[0].handle].organization == organization)


def filter_by_country(ranklist_row, handle_to_user_mapping, country):
    return (r for r in ranklist_row if handle_to_user_mapping[r.party.members[0].handle].country == country)


def main():
    api = CodeforcesAPI()

    contests = api.contest_list()
    kz_users = set()
    for contest in contests:
        try:
            ranklist = api.contest_standings(contest.id, count=1000)
        except:
            continue
        ranklist_rows = list(ranklist['rows'])
        contest_user_handles = list(get_all_user_handles(ranklist_rows))
        for i in range(0,len(contest_user_handles),100):
            try:
                batch_users = contest_user_handles[i:min(i+100,len(contest_user_handles))]
                time.sleep(3)
                batch_kz_users_info = {u.handle: u for u in api.user_info(batch_users) if u.country=="Kazakhstan"}
                for handle, user in batch_kz_users_info.items():
                    print('handle {}, rating {}'.format(handle, user.rating))
                    kz_users.add((user.rating, handle))
            except:
                time.sleep(10)

    print("Top codeforces user from Kazakhstan:")
    list_top_100 = []
    for i in range(min(100, len(kz_users))):
        max_kz_user = max(kz_users)
        print('{}. {}({})'.format(i + 1, max_kz_user[1], max_kz_user[0]))
        list_top_100.append(max_kz_user)
        kz_users.remove(max_kz_user)
    print('Average rating of top {} is {}'.format(len(list_top_100), sum([rating for rating, _ in list_top_100])/len(list_top_100)))

if __name__ == '__main__':
    main()
