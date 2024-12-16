#!/bin/env/python3

import argparse
import os

import struct
import numpy as np

import json


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert spacev1b binary files to JSON files')

    parser.add_argument('--query', type=str, help='Path to query vector binary file')
    parser.add_argument('--gt', type=str, help='Path to ground truth binary file')
    parser.add_argument('--distance', type=str, help='Path to distance binary file')

    args = parser.parse_args()

    # 
    # Load base vectors
    #   Base vector does not need to be loaded, 
    # 

    # We assume it uses the AnnCompoundReader of the vector-db-benchmark
    #   https://github.com/qdrant/vector-db-benchmark

    #
    # Load query vectors
    query_vec_f = open(args.query, 'rb')

    # 
    # Convert it to JSON
    query_vec_count = struct.unpack('i', query_vec_f.read(4))[0]
    query_vec_dimension = struct.unpack('i', query_vec_f.read(4))[0]

    query_vec = np.frombuffer(
        query_vec_f.read(query_vec_count * query_vec_dimension), dtype=np.int8).reshape((query_vec_count, query_vec_dimension)
        )

    print(f"Query vector shape: {query_vec.shape}, type: {query_vec.dtype}")
    
    query_vec_f.close()

    # 
    # Load ground truth
    ground_truth_f = open(args.gt, 'rb')
    
    ground_truth_count = struct.unpack('i', ground_truth_f.read(4))[0]
    ground_truth_topk = struct.unpack('i', ground_truth_f.read(4))[0]

    ground_truth = np.frombuffer(
        ground_truth_f.read(ground_truth_count * ground_truth_topk * 4), dtype=np.int32).reshape((ground_truth_count, ground_truth_topk)
    )

    print(f"Ground truth shape: {ground_truth.shape}")

    ground_truth_f.close()

    # Sample print
    print(f"Query sample: {query_vec[0]}")
    print(f"Ground truth sample: {ground_truth[0]}: type: {ground_truth.dtype}")


    # 
    # Load distance
    distance_f = open(args.distance, 'rb')

    distance_count = struct.unpack('i', distance_f.read(4))[0]
    distance_topk = struct.unpack('i', distance_f.read(4))[0]

    distance = np.frombuffer(
        distance_f.read(distance_count * distance_topk * 4), dtype=np.float32).reshape((distance_count, distance_topk)
    )

    print(f"Distance shape: {distance.shape}")

    distance_f.close()


    # Set the query format : Example
    # {
    #     "query": [0.5806249976158142, 0.4124372899532318, ...], 
    #     "conditions": {
    #             "and": [{"a": {"match": {"value": 53}}}]
    #     }, 
    #     "closest_ids": [635408, 97779, 223433, ...], 
    #     "closest_scores": [0.8599298000335693, 0.8457251191139221, ...]
    # }
    # 
    # ln -s $HOME/sjoon/msra-workspace/dataset/SPACEV1B/vectors.bin/vectors.bin.npy vectors.npy
    # python3 -m run --engines pgvector-default
    # python3 -m run --engines pgvector-default --skip-upload

    # Need to export the query vectors and ground truth to JSON
    #  In the file, each line is a JSON object
    #  Example:
    # python3.12 spacev1b-query-to-json.py --query ../dataset/extended-full-set/spacev1b-query-log-extended.bin --gt ../dataset/extended-full-set/spacev1b-query-log-truth-extended.bin --distance ../dataset/extended-full-set/spacev1b-query-dist-extended.bin

    export_file = "tests.jsonl"
    
    # Export query vectors
    with open(export_file, 'w') as query_f:
        for i in range(query_vec_count):
            query_f.write(json.dumps({
                "query": query_vec[i].tolist(),
                "conditions": {},
                "closest_ids": ground_truth[i].tolist(),
                "closest_scores": distance[i].tolist()
            }))
            query_f.write("\n")
    
    print(f"Exported query vectors to {export_file}")

    # Export ground truth
