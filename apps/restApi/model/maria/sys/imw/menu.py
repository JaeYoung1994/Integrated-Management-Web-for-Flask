from common.db.mariaDB import MariaDB


class Menu(MariaDB):
    '''
        SQL: 메인 메뉴 정보
        SQL: Main Menu Information
        author: 이재영 (Jae Young Lee)
    '''
    def getMainMenuList(cls, account):
        rv = {'result': False}
        try:
            cls.connect()
            curs = cls._dbConn.cursor()
            sql = '''
                SELECT `id`, `name`, `url`, `depth`, `pid`, `order` FROM sys_menu
                WHERE `usedYN` = 'Y' 
                AND (`id` IN (
                       SELECT `id` 
                       FROM auth_menu 
                       WHERE `type` = 'authority' 
                       AND `code` = (SELECT `authority` FROM `user` WHERE email = '%s')
                   )
                   OR `id` IN (
                       SELECT `id` 
                       FROM auth_menu 
                       WHERE `type` = 'group' 
                       AND `code` = (SELECT `group` FROM `user` WHERE email = '%s')
                   )
                )
                ORDER BY `depth`, `pid`, `order`
            ''' % (account["email"], account["email"])
            curs.execute(sql)
            rv['result'] = True
            rv['data'] = curs.fetchall()
        except Exception as ex:
            rv['msg'] = ex
        finally:
            if curs:
                curs.close()
            return rv