import numpy as np
import pandas as pd
import joblib
import os
import psutil
import random

class DetectKeylogger():
    def predict():
        path='keylogger_model.pkl'
        model=joblib.load(path,'rb')

        running_processes = len(psutil.pids())

        stats=psutil.net_io_counters()
        
        packets_sent=stats.packets_sent

        packets_received=stats.packets_recv

        bytes_sent=stats.bytes_sent

        bytes_received=stats.bytes_recv

        source_port= random.randint(4,65536)

        init_win_byres_forward= random.randint(1262,65536)

        init_win_bytes_backward= random.randint(1262,65536)
    
        flow_duration= random.randint(0,100000)

        flow_iat_max= random.randint(0,100000)

        flow_iat_min= random.randint(0,100000)

        df=pd.DataFrame({'packets_sent':[packets_sent],'packets_received':[packets_received],'bytes_sent':[bytes_sent],'bytes_received':[bytes_received],'source_port':[source_port],'init_win_bytes_forward':[init_win_byres_forward],'init_win_bytes_backward':[init_win_bytes_backward],'flow_duration':[flow_duration],'flow_iat_min':[flow_iat_min],'running_processes':[running_processes],'flow_iat_max':[flow_iat_max]})

        scaler=joblib.load('keylogger_scaler.pkl','rb')
        scaler.fit(df)
        scaled_features = scaler.transform(df)

        prediction=model.predict(scaled_features)
        prediction=round(prediction[0])

        return prediction





