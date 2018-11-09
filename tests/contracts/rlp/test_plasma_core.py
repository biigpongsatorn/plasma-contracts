import pytest
from plasma_core.transaction import Transaction


@pytest.fixture
def plasma_core_test(ethtester, get_contract):
    contract = get_contract('PlasmaCoreTest')
    ethtester.chain.mine()
    return contract


def test_slice_proof(plasma_core_test):
    proof = b'\x00' * 63 + b'\x01'
    assert plasma_core_test.sliceProof(proof, 0) == proof[0:32]
    assert plasma_core_test.sliceProof(proof, 1) == proof[32:64]


def test_slice_signature(plasma_core_test):
    signatures = b'\x00' * 129 + b'\x01'
    assert plasma_core_test.sliceSignature(signatures, 0) == signatures[0:65]
    assert plasma_core_test.sliceSignature(signatures, 1) == signatures[65:130]


def test_get_output(plasma_core_test):
    owner = b'0x82a978b3f5962a5b0957d9ee9eef472ee55b42f1'
    amount = 100
    tx = Transaction(outputs=[(owner, amount)])
    assert plasma_core_test.getOutput(tx.encoded, 0) == [owner.decode("utf-8"), amount]
    assert plasma_core_test.getOutput(tx.encoded, 1) == ['0x0000000000000000000000000000000000000000', 0]


def test_get_input_id(plasma_core_test):
    input_id = (2, 2, 2)
    tx = Transaction(inputs=[input_id])
    assert plasma_core_test.getInputId(tx.encoded, 0) == tx.inputs[0].identifier
    assert plasma_core_test.getInputId(tx.encoded, 1) == tx.inputs[1].identifier


def test_get_output_index(plasma_core_test):
    output_id = 1000020003
    assert plasma_core_test.getOindex(output_id) == 3


def test_get_tx_index(plasma_core_test):
    output_id = 1000020003
    assert plasma_core_test.getTxindex(output_id) == 2


def test_get_blknum(plasma_core_test):
    output_id = 1000020003
    assert plasma_core_test.getBlknum(output_id) == 1

def test_deposit_parsing(plasma_core_test):
    hexed = "0xf86fd0c3808080c3808080c3808080c3808080f85cd69482a978b3f5962a5b0957d9ee9eef472ee55b42f164d694000000000000000000000000000000000000000080d694000000000000000000000000000000000000000080d694000000000000000000000000000000000000000080"
    from eth_utils import decode_hex
    raw = decode_hex(hexed)
    o0 = plasma_core_test.getOutput(raw, 0)
    o1 = plasma_core_test.getOutput(raw, 1)
    o2 = plasma_core_test.getOutput(raw, 2)
    o3 = plasma_core_test.getOutput(raw, 3)
    print("output 0 is {}".format(o0))
    print("output 1 is {}".format(o1))
    print("output 2 is {}".format(o2))
    print("output 3 is {}".format(o3))
    assert False
