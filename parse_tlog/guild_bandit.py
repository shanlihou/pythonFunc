import Filter

if __name__ == '__main__':
    whole_log = r'E:\shLog\tlog\xzj.log.LOG_GUILD_BANDIT.log'
    filter_inner_name = r'E:\shLog\tlog\dev_openids.txt'
    filter_out_name = r'E:\shLog\tlog\11-11.txt'
    f = Filter.Filter(whole_log, filter_inner_name, filter_out_name)
    # f.filter_tlog(r'E:\shLog\tlog\xzj.log', 'LOG_VITALITY')
    f.filter_guild_bandit()

