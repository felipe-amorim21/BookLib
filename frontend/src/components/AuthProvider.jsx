import PropTypes from 'prop-types'; // import PropTypes
import { AuthProvider } from '../context/AuthContext';
import React from 'react';

function AuthWrapper({ children }) {
  return <AuthProvider>{children}</AuthProvider>;
}


AuthWrapper.propTypes = {
  children: PropTypes.node.isRequired, 
};

export default AuthWrapper;
