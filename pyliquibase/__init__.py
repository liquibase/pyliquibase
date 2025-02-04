import logging
import os
import sys

#####  loggger
log = logging.getLogger(name="pyliquibase")
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


#####


class Pyliquibase():

    def __init__(self, defaultsFile: str, liquibaseHubMode: str = "off", logLevel: str = None):

        self.args = []
        if defaultsFile:
            self.args.append("--defaults-file=%s" % defaultsFile)

        if liquibaseHubMode:
            self.args.append("--hub-mode=%s" % liquibaseHubMode)

        if logLevel:
            self.args.append("--log-level=%s" % logLevel)

        self.cli = self._cli()

    def _cli(self):
        ##### jnius
        import jnius_config
        from pkg_resources import resource_filename

        LIQUIBASE_CLASSPATH: list = [os.getcwd() + "/",
                                     resource_filename(__package__, "liquibase/liquibase.jar"),
                                     resource_filename(__package__, "liquibase/lib/*"),
                                     resource_filename(__package__, "liquibase/lib/picocli*"),
                                     resource_filename(__package__, "jdbc-drivers/*")]

        if not jnius_config.vm_running:
            jnius_config.add_classpath(*LIQUIBASE_CLASSPATH)
        else:
            log.warning("VM is already running, can't set classpath/options; VM started at" + jnius_config.vm_started_at)

        from jnius import JavaClass, MetaJavaClass, JavaMethod
        #####
        class LiquibaseCommandLine(JavaClass, metaclass=MetaJavaClass):
            __javaclass__ = 'liquibase/integration/commandline/LiquibaseCommandLine'

            # methods
            execute = JavaMethod('([Ljava/lang/String;)I')

        return LiquibaseCommandLine()

    def execute(self, *arguments: str):
        log.debug("Executing liquibase %s" % arguments)
        rc = self.cli.execute(self.args + list(arguments))
        if rc:
            raise Exception("Liquibase execution failed with exit code:%s" % rc)

    def addarg(self, key:str, val):
        _new_arg="%s=%s" % (key, val)
        self.args.append(_new_arg)

    def update(self):
        self.execute("update")

    def updateSQL(self):
        self.execute("updateSQL")

    def validate(self):
        self.execute("validate")

    def status(self):
        self.execute("status")

    def rollback(self, tag):
        log.debug("Rolling back to tag:%s" % tag)
        self.execute("rollback", tag)

    def rollback_to_datetime(self, datetime):
        log.debug("Rolling back to %s" % str(datetime))
        self.execute("rollbackToDate", datetime)
