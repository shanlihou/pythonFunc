import utils
import const


if __name__ == '__main__':
    fname = utils.filter_tlog(const.ORI_FILE_NAME, 'GuildFlow')
    fname = utils.filter_tlog(const.ORI_FILE_NAME, 'LOG_GUILD_MEMBER_OPR')
    fname = utils.filter_tlog(const.ORI_FILE_NAME, 'LOG_GUILD_OPR')
