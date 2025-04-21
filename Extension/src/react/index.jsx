import React from 'react';
import ReactDOM from 'react-dom';
import Popup from './components/popup';
import {createRoot} from 'react-dom/client';
import { ChakraProvider } from '@chakra-ui/react';
const root = createRoot(document.getElementById('root'));

root.render(
    <React.StrictMode>
      <ChakraProvider>
        <Popup />
      </ChakraProvider>
    </React.StrictMode>
  );