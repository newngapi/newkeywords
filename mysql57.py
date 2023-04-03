
import mysql.connector

#INSERT INTO `cscscs1`.`channels` (`id`, `channel_id`, `channel_name`, `channel_title`, `channel_is_megagroup`, `channel_is_group`, `channel_is_broadcast`, `channel_count`, `channel_access_hash`, `updatetime`) VALUES (1, 112121212121, 'dgffd', 'dfgdgfd', 0, 0, 1, 11111, '12453366365363', '2023-03-31 20:06:46')



def execute_database_operation(operation, data, connection):
    try:
        # Create a cursor
        cursor = connection.cursor(dictionary=True)

        # Execute the operation
        if operation == 'insert':
            sql = "INSERT INTO channels (channel_id, channel_name, channel_title, channel_is_megagroup, " \
                  "channel_is_group, channel_is_broadcast, channel_count, channel_access_hash, updatetime) " \
                  "VALUES (%(channel_id)s, %(channel_name)s, %(channel_title)s, %(channel_is_megagroup)s, " \
                  "%(channel_is_group)s, %(channel_is_broadcast)s, %(channel_count)s, %(channel_access_hash)s, " \
                  "%(updatetime)s)"
            cursor.execute(sql, data)
            connection.commit()
            return True
        elif operation == 'select':
            sql = "SELECT * FROM channels WHERE channel_id=%s"
            cursor.execute(sql, (data,))
            result = cursor.fetchone()
            return result
        else:
            return False
    except mysql.connector.Error as error:
        print("Failed to execute operation: {}".format(error))
        return False
    finally:
        # Close the cursor (the connection should be closed outside this function)
        cursor.close()


def msg_database_operation(operation, data, connection):
    try:
        # Create a cursor
        cursor = connection.cursor(dictionary=True)

        # Execute the operation
        if operation == 'insert':
            sql = "INSERT INTO `message` (`user_id`, `chat_id`, `channel_id`, `msgid`, `username`, `msg_url`, `chat_title`, `keywords`, `text`, `status`, `updatetime`) VALUES (%(user_id)s, %(chat_id)s, %(channel_id)s, %(msgid)s, %(username)s, %(msg_url)s, %(chat_title)s, %(keywords)s, %(text)s, %(status)s, %(updatetime)s)"                   
            # sql = "INSERT INTO message (chat_id, channel_id, msgid, username,channel_msg_url," \
            #       "chat_title, text, status, updatetime) VALUES (%(chat_id)s, %(channel_id)s, %(msgid)s, " \
            #       "%(username)s, %(channel_msg_url)s, %(chat_title)s, %(text)s, %(status)s, %(updatetime)s) "
            print(sql)
            cursor.execute(sql, data)
            connection.commit()
            return True
        elif operation == 'select':
            sql = "SELECT * FROM message WHERE msgid=%s"
            cursor.execute(sql, (data,))
            result = cursor.fetchone()
            return result
        else:
            return False
    except mysql.connector.Error as error:
        print("Failed to execute operation: {}".format(error))
        return False
    finally:
        # Close the cursor (the connection should be closed outside this function)
        cursor.close()