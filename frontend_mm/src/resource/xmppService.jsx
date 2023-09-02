import {Strophe} from 'strophe.js';

const xmppService = {
    connection: null,

    connect: (jid, password, onMessageReceived) => {
        xmppService.connection = new Strophe.Connection({
            jid,
            password,
        });

        xmppService.connection.connect(jid, password, (status) => {
            if (status === Strophe.Status.CONNECTED) {
                console.log('Connected to XMPP server');
                xmppService.connection.addHandler(onMessageReceived, null, 'message', 'chat');
            }
        });
    },

    sendMessage: (toJid, message) => {
        const msg = Strophe.xmlElement('message', [
            ['to', toJid],
            ['type', 'chat'],
        ]);
        msg.c('body', {}, message);
        xmppService.connection.send(msg);
    },

    disconnect: () => {
        if (xmppService.connection) {
            xmppService.connection.disconnect();
            xmppService.connection = null;
        }
    },
};

export default xmppService;
