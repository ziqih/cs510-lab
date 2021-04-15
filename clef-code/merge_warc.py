import os
import pickle
import argparse
import shutil
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('sample_dir')
    parser.add_argument('output_path')
    args = parser.parse_args()

    rec_dir = os.path.join(args.sample_dir, 'rec')
    warc_dir = os.path.join(args.sample_dir, 'warc')

    existing_domain_dirs = set(os.listdir(warc_dir))

    collected = []
    for rec_file in os.listdir(rec_dir):
        print ('processing: ', rec_file)

        rec_file = os.path.join(rec_dir, rec_file)
        with open(rec_file, 'rb') as f:
            recs = pickle.load(f)

        for rec in recs:
            if not rec.get('directory', None):
                continue

            if not rec.get('uri', None):
                continue

            domain_dir = os.path.split(rec['directory'])[-1]
            warc_file = os.path.join(warc_dir, domain_dir, rec['uri'])
            if domain_dir not in existing_domain_dirs:
                continue

            if not os.path.exists(warc_file):
                continue

            row = [
                rec['url'],
                rec['timestamp'],
                rec.get('charset', 'utf-8'),
                domain_dir,
                rec['uri'],

                rec['filename'],
                rec['offset'],
                rec['length'],
                rec['digest'],
            ]
            collected.append(row)

    collected = pd.DataFrame(collected, columns=[
        'url', 'timestamp', 'charset', 'domain', 'uri',
        'filename', 'offset', 'length', 'digest'
    ])
    print ('collected #: ', collected.shape[0])
    collected.to_pickle(args.output_path)
