#https://solanacookbook.com/guides/retrying-transactions.html#an-in-depth-look-at-sendtransaction
#can poll for signature status
'''A common pattern for manually retrying transactions involves temporarily storing the lastValidBlockHeight that comes from getLatestBlockhash. Once stashed, an application can then poll the cluster’s blockheight and manually retry the transaction at an appropriate interval.'''
#https://solanacookbook.com/guides/retrying-transactions.html#when-to-re-sign-transactions
'''In Solana, a dropped transaction can be safely discarded once the blockhash it references is older than the lastValidBlockHeight received from getLatestBlockhash. Developers should keep track of this lastValidBlockHeight by querying getEpochInfo and comparing with blockHeight in the response. Once a blockhash is invalidated, clients may re-sign with a newly-queried blockhash.'''
from enum import Enum
from solana.rpc.api import Client
from solana.rpc.types import RPCResponse
from configchaininfo import SOLANA_MAINNET_HTTP_ENDPOINT as RPC_URL

TxStatus = Enum('TxStatus','NOTPROCESSED PROCESSED CONFIRMED FINALIZED FAILED')
class SolanaInfo:
    st2status_d = {'processed': TxStatus.PROCESSED, 'confirmed': TxStatus.CONFIRMED,
    'finalized': TxStatus.FINALIZED}
    #https://docs.solana.com/developing/clients/jsonrpc-api
    def __init__(self, curclient: Client = None) -> None:
        self.client = curclient or Client(RPC_URL)
        self.last_err = None
    def parse_rpc_result(self, rsp: RPCResponse):
        try:
            return rsp['result']
        except KeyError:
            try:
                self.last_err = rsp['error']
            except KeyError:
                self.last_err = rsp
            return
                
    def fetch_cur_blockheight(self):
        return self.parse_rpc_result(self.client.get_epoch_info())['blockHeight']

    def fetch_tx_statuses(self, signatures: list[str]):
        '''Send an RPC query and get a list of TxStatus enum objects, or None if sending the query throws.
        
        Status UNKNOWN means unknown transaction, such when it was sent but not yet processed, so can't be found in the 
        block explorer'''
        #https://docs.solana.com/developing/clients/jsonrpc-api#getsignaturestatuses
        try:
            statuses = self.parse_rpc_result(self.client.get_signature_statuses(signatures))['value']
            assert len(statuses) == len(signatures)
        except Exception as e: 
            #network error or rpc response doesn't have a 'result' field or 'result' doesn't have a 'value' field
            #TODO maybe different codes for tx error vs network error 
            return 
        return [self._process_tx_status(x) for x in statuses]
    
    def fetch_tx_status_dict(self, signatures: list[str]) -> dict[str, TxStatus]:
        if (txstatuses := self.fetch_tx_statuses(signatures)) is None:
            return 
        assert len(txstatuses) == len(signatures)        
        return {sig: txstatus for sig, txstatus in zip(signatures, txstatuses)}

    def _process_tx_status(self, status) -> TxStatus:
        if not status:
            return TxStatus.NOTPROCESSED #tx not yet found in explorer
        if status['err']:
            return TxStatus.FAILED
        return self.st2status_d[status['confirmationStatus']]
        

if __name__ == '__main__':
    solinfo = SolanaInfo()
    import time
    while True:
        #print(f'{client.get_epoch_info()=}\n\n{client.get_recent_blockhash()=}\n\n')
        print(solinfo.fetch_cur_blockheight())
