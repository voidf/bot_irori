
class Configuration():
    # Server
    bind_port = 18082
    buffer = 4096
    idle_tle = 70
    heartbeat_time = 30
    quic_key = 'public'
    quic_admin_key = 'admin'
    # Worker
    quic_port = 18082
    quic_host = '127.0.0.1'
    max_worker = 4