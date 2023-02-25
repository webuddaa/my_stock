
ps x | grep 'run_select_futures_15m_5m' | grep -v grep | awk '{print $1}' | xargs kill -9
