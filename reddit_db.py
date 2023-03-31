import sqlite3


try:
    sqliteConnection = sqlite3.connect('sam_bot.db',timeout=10)
    # sqliteConnection.execute("PRAGMA journal_mode=WAL")
    cursor = sqliteConnection.cursor()
    print("Successfully connected ")
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
def insert_comment( encounter ):
    """Inserts unique comment to database """
   
    try:
        
        cursor.execute( 'INSERT INTO  reddit_comments ('+encounter.get_param_string()+') VALUES ('+encounter.get_replace_string()+')', encounter.get_tuple() )
        print("SUCCESSFULLY INSERTED ",encounter.id, " into reddit_comments")
        sqliteConnection.commit()
        return True
       
    except Exception as e:
         print( 'Error inserting encounter:', encounter.id, e )
         sqliteConnection.close()
         return False
    
    
def get_comment_ids():
    comment_ids = []
    try:
        for row in cursor.execute("SELECT id from reddit_comments"):
            comment_ids.append(row[0])
    except Exception as e:
        sqliteConnection.close()
        print("ERROR retrieving from reddit_comments",e)
        return  "Broken"
    return comment_ids
def get_comment_parent_ids():
    comment_parent_ids = []
    try:
        for row in cursor.execute("SELECT parentId from reddit_comments"):
            comment_parent_ids.append(row[0])
    except Exception as e:
        sqliteConnection.close()
        print("ERROR retrieving from reddit_comments",e)
        return  "Broken"
    return comment_parent_ids
def get_subredits():
    subredits = []
    try:
        for row in cursor.execute("SELECT subreddit from reddit_comments"):
            
            subredits.append(row[0])
    except Exception as e:
        sqliteConnection.close()
        print("ERROR retrieving from reddit_comments",e)
        return  "Broken"
    return list(set(subredits))

def get_comment_bodys(num_comments=0):
    comment_bodys = []
    i = 0
    try:
        for row in cursor.execute("SELECT body from reddit_comments"):
            if(i >= num_comments and num_comments != 0):
                break
            comment_bodys.append(row[0])
            i+= 1
    except Exception as e:
        sqliteConnection.close()
        print("ERROR retrieving from reddit_comments",e)
        return  "Broken"
    return comment_bodys
def get_comments():
    comments = []
    try:
        for row in cursor.execute("SELECT body, created, id, parentId, subreddit from reddit_comments"):
            comment =  RedditComment(row[0],row[1],row[2],row[3],row[4])
            comments.append(comment)
            i+= 1
    except Exception as e:
        sqliteConnection.close()
        print("ERROR retrieving from reddit_comments",e)
        return  "Broken"
    return comments
def get_comment(parentId):
    # try:
    comment = None
    for row in cursor.execute("SELECT  body, created, id, parentId, subreddit from reddit_comments WHERE id=?",(parentId,)):
        comment =  RedditComment(row[0],row[1],row[2],row[3],row[4])
        
    # except Exception as e:
    #     sqliteConnection.close()
    #     print("ERROR retrieving from reddit_comments",e)
    #     return  "Broken"
    return comment
def get_sub_comments(subredit):
    # try:
    comments = []
    for row in cursor.execute("SELECT  body from reddit_comments WHERE subreddit=?",(subredit,)):
        comments.append(row[0])
        
    # except Exception as e:
    #     sqliteConnection.close()
    #     print("ERROR retrieving from reddit_comments",e)
    #     return  "Broken"
    return comments
    
def get_submission_ids():
    submissions_ids = []
    try:
        for row in cursor.execute("SELECT id from reddit_submissions"):
            submissions_ids.append(row[0])
    except Exception as e:
        # sqliteConnection.close()
        print("ERROR retrieving from reddit_submissions",e)
        return  "Broken"
    return submissions_ids
def get_submissions():
    submissions = []
    # try:
    for row in cursor.execute("SELECT created, id, selftext, subreddit,title from reddit_submissions"):
        submission = RedditSubmission(row[0],row[1],row[2],row[3],row[4])
        submissions.append(submission)
    # except Exception as e:
    #     # sqliteConnection.close()
    #     print("ERROR retrieving from reddit_submissions",e)
    #     return  "Broken"
    return submissions
def get_submission(id):
    submission = None
    # try:
    for row in cursor.execute("SELECT created, id, selftext, subreddit,title from reddit_submissions WHERE id=?",(id,)):
        submission = RedditSubmission(row[0],row[1],row[2],row[3],row[4])
          
    # except Exception as e:
    #     sqliteConnection.close()
    #     print("ERROR retrieving from reddit_submissions",e)
    #     return  "Broken"
    return submission
def insert_submission( encounter ):
    """Inserts unique submission to database """
   
    try:
        
        cursor.execute( 'INSERT INTO  reddit_submissions ('+encounter.get_param_string()+') VALUES ('+encounter.get_replace_string()+')', encounter.get_tuple() )
        print("SUCCESSFULLY INSERTED ",encounter.id, " into reddit_submissions")
        sqliteConnection.commit()
        return True
       
    except Exception as e:
        print( 'Error inserting encounter:', encounter.id, e )
        sqliteConnection.close()
        return False
       
        
    
class RedditComment:
    """Class that stores all """
    def __init__( self, *args ):
        self.__index = 0
        self.body= self.get_next_arg( args )
        self.created = self.get_next_arg( args )
        self.id = self.get_next_arg( args )
        self.parentId = self.get_next_arg( args )
        self.subreddit =  self.get_next_arg( args )
     

    

    def get_param_string( self ):
        return ( "body"+
            ", created"+
            ", id"+
            ", parentId"+
            ", subreddit"
            )

    def get_replace_string( self ):
        return ( "?"+
            ", ?"+
            ", ?"+
            ", ?"+
            ", ?")
    
    def get_tuple( self ):
        dict = self.__dict__
        values = list(dict.values())
        values.pop(0)
        return tuple(values)
    # def __str__(self):
    #     return "ticket_id: %s, assignee: %s, win_probability: %s, amount_currency: %s, amount: %s,  start_date: %s, close_date: %s, stage: %s, owner: %s" %( self.ticket_id,
    #         self.assignee,
    #         self.win_probability,
    #         self.amount_currency,
    #         self.amount,
    #        self.start_date,
    #        self.close_date,
    #        self.stage,
    #        self.owner)
    def get_next_arg( self, args ):
        if len(args) <= self.__index:
            return None
        value = args[self.__index]
        self.__index += 1
        return value
    def update( self, cursor ):
        #updates opportunities with new info
        cursor.execute( 'UPDATE reddit_comments SET (' + self.get_param_string() + ') = (' + self.get_replace_string() + ') WHERE id = %s', self.get_tuple() + (self.id,) )
class RedditSubmission:
    """Class that stores all """
    def __init__( self, *args ):
        self.__index = 0
        self.created= self.get_next_arg( args )
        self.id = self.get_next_arg( args )
        self.selftext = self.get_next_arg( args )
        self.subreddit = self.get_next_arg( args )
        self.title =  self.get_next_arg( args )
     

    

    def get_param_string( self ):
        return ( "created"+
            ", id"+
            ", selftext"+
            ", subreddit"+
            ", title"
            )

    def get_replace_string( self ):
        return ( "?"+
            ", ?"+
            ", ?"+
            ", ?"+
            ", ?")
    
    def get_tuple( self ):
        dict = self.__dict__
        values = list(dict.values())
        values.pop(0)
        return tuple(values)

    def get_next_arg( self, args ):
        if len(args) <= self.__index:
            return None
        value = args[self.__index]
        self.__index += 1
        return value
    def update( self, cursor ):
        #updates reddit_submissions with new info
        cursor.execute( 'UPDATE reddit_submissions SET (' + self.get_param_string() + ') = (' + self.get_replace_string() + ') WHERE id = %s', self.get_tuple() + (self.id,) )
 