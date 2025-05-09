"""
    c3sdb/build_utils/src_data.py

    Dylan Ross (dylan.ross@pnnl.gov)

    Module for adding source datasets to the database
"""


import hashlib
import re
import json
import sqlite3
import os


# path to built in source dataset directory
_SRC_DATA_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_include/src_data/")


def _gen_id(name: str, 
            adduct: str, 
            ccs: float, 
            ccs_type: str, 
            src_tag: str
            ) -> str :
    """ 
    computes a unique string identifier for an entry by hashing on name+adduct+ccs+ccs_type+src_tag
    """
    s = f"{name}{adduct}{ccs}{ccs_type}{src_tag}"
    h = hashlib.sha1(s.encode()).hexdigest()[-10:].upper()
    return 'CCSBASE_' + h


def add_dataset(cursor: sqlite3.Cursor, 
                src_tag: str
                ) -> int :
    """
    Adds values from a source dataset (a JSON file identified by src_tag) to the database
    
    Parameters
    ----------
    cursor : ``sqlite3.cursor``
        cursor for C3S.db
    src_tag : ``str``
        identifier for source dataset (JSON file)
    
    Returns
    -------
    n_added : ``int``
        number of entries added to the database from this source
    """
    # ensure the specified dataset exists
    src_dset_file = os.path.join(_SRC_DATA_PATH, f"{src_tag}.json")
    if not os.path.isfile(src_dset_file):
        msg = (f"add_dataset: dataset with src_tag: {src_tag} not found")
        raise ValueError(msg)
    with open(src_dset_file, "r") as j:
        jdata = json.load(j)
    # regex for identifying multiple charges
    multi_z = re.compile('.*[]]([0-9])[+-]')
    # track g_ids
    g_ids = set()
    # track how many entries added to the database
    added = 0
    # query string
    # g_id, name, adduct, mz, ccs, smi, src_tag
    qry = "INSERT INTO master VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
    for cmpd in jdata["data"]:
        # strip whitespace off of the name
        name = cmpd["name"].strip()
        # fix messed up adducts on the fly
        adduct = cmpd["adduct"]
        adduct = {
            "[M+]+": "[M]+", 
            "M+NH4]+": "[M+NH4]+",
            "[M+H]+*": "[M+H]+",
            "[M+Na]+*": "[M+Na]+",
            "[M+H20-H]-": "[M+H2O-H]-",
        }.get(adduct, adduct)
        # check for multiple charges
        mz = float(cmpd.get("mz", float(cmpd.get("m/z", 0))))  # finds m/z if null, then default to 0

        is_multi = multi_z.match(adduct)
        z = 1
        if is_multi:
            z = int(is_multi.group(1))
        # calculate the mass
        mass = mz * z
        # use smi if included
        smi = cmpd.get("smi")
        # make sure CCS is a float
        ccs = float(cmpd["ccs"])
        # metadata
        ccs_type, ccs_method = jdata["metadata"]["ccs_type"], jdata["metadata"]["ccs_method"]
        src_tag = jdata["metadata"]["src_tag"]
        # unique identifier
        g_id = _gen_id(name, adduct, ccs, ccs_type, src_tag)
        if g_id not in g_ids:
            # implicitly skip duplicate g_ids
            qdata = (
                g_id, name, adduct, mass, z, mz, ccs, smi, None, src_tag, ccs_type, ccs_method
            )
            cursor.execute(qry, qdata)
            g_ids.add(g_id)
            added += 1
    # return the number of entries added to the database from this dataset
    return added
        
