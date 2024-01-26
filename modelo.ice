module SMPC{
    interface Servidor {
        void messageFromClient(int part, 
            out int partServer, 
            out int sumServer
        );
        void messageFromDummy(int sumDummy);
        void finalize(int sumClient, byte message);
    }

    interface Dummy {
        void messageFromClient(int part, 
            out int partDummy, 
            out int sumDummy
        );
        void messageFromServer(int part, 
            out int partDummy
        );
    }
}