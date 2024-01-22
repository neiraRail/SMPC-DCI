module SMPC{
    interface Servidor {
        void entregarDesdeCliente(int parte, 
            out int parteServer, 
            out int sumaServer
        );
        void entregarDesdeDummy(int suma);
        void finalizar(int suma, byte payload);
    }

    interface Dummy {
        void entregarDesdeCliente(int parte, 
            out int parteDummy, 
            out int sumaDummy
        );
        void entregarDesdeServer(int parte, 
            out int parteDummy
        );
    }
}