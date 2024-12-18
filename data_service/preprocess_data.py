def preprocess_data(raw_data):
    # Example transformation
    for record in raw_data:
        record["timestamp"] = record.pop("datetime")
    return raw_data
