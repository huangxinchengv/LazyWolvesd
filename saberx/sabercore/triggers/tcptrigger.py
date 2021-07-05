from triggerbase import TriggerBase
from tcphandler import TCPHandler

class TCPTrigger(TriggerBase):
	def __init__(self, **kwargs):
		TriggerBase.__init__(type=kwargs.get("type"), check=kwargs.get("check"), negate=kwargs.get("negate"))

		if kwargs.get("host"):
			self.host = kwargs.get("host")
		if kwargs.get("port"):
			self.port = kwargs.get("port", 80)
        if kwargs.get("timeout"):
            self.timeout = kwargs.get("timeout", 5)
		if kwargs.get("attempts"):
			self.attempts = kwargs.get("attempts", 1)
		if kwargs.get("threshold"):
			self.threshold = kwargs.get("threshold", 1)
        if kwargs.get("ssl"):
            self.ssl = kwargs.get("ssl", False)

		self.valid_checks = ["tcp_connect", "tcp_fail"]

        self.PORT_MIN, self.PORT_MAX = 0, 65535

    def fire_trigger(self):
        if not self.sanitise():
            return False, "IMPROPER_ARGUMENTS"

        trigerred, error = TCPHandler.check_connection(host=self.host, port=self.port, timeout=self.timeout, attempts=self.attempts, threshold=self.threshold, check_type=self.check, ssl=self.ssl)

        return self.eval_negate(trigerred, error)

    def sanitise(self):
        if not self.host:

            '''
                Log error
            '''
            return False
        
        if self.port < self.PORT_MIN or self.port > self.PORT_MAX:
            
            '''
                Log error
            '''
            return False

        if self.timeout <= 0:

            '''
                Log error
            '''
            return False

        if self.attempts <= 0:

            '''
                Log error
            '''
            return False

        if self.threshold <= 0:

            '''
                Log error
            '''
            return False

        if self.check not in self.valid_checks:

            '''
                Log error
            '''
            return False

