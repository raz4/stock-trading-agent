import React from 'react';
import { Pane, Tab, Text } from 'evergreen-ui';
import { Link, withRouter } from 'react-router-dom';
import * as firebase from "firebase/app";
import "firebase/auth";

class Header extends React.Component {
    constructor(props) {
        super(props);

        const firebaseConfig = {
            apiKey: "AIzaSyDyXgmt0I2hhAH_kINktiqQzyfo8vj8UXI",
            authDomain: "qualified-sun-271304.firebaseapp.com",
            databaseURL: "https://qualified-sun-271304.firebaseio.com",
            projectId: "qualified-sun-271304",
            storageBucket: "qualified-sun-271304.appspot.com",
            messagingSenderId: "15484625972",
            appId: "1:15484625972:web:4b188c7ffbcfe0cfbe9661",
            measurementId: "G-KT2NJHT2L5"
        };
        // Initialize Firebase
        if (!firebase.apps.length) {
            firebase.initializeApp(firebaseConfig);
        }
        // firebase.analytics();

        const localAccessToken = localStorage.getItem('accessToken');
        const localUser = JSON.parse(localStorage.getItem('user'));
        if (localAccessToken && localUser) {
            this.state = {
                auth: {
                    accessToken: localAccessToken,
                    user: localUser
                }
            }
        } else {
            this.state = {
                auth: {
                    accessToken: null,
                    user: null
                }
            };
        }
    }

    login() {
        const provider = new firebase.auth.GoogleAuthProvider();
        firebase.auth().signInWithPopup(provider).then((result) => {
            // This gives you a Google Access Token. You can use it to access the Google API.
            localStorage.setItem('accessToken', result.credential.accessToken)
            // The signed-in user info.
            localStorage.setItem('user', JSON.stringify(result.user))
            this.setState({
                auth: {
                    accessToken: result.credential.accessToken,
                    user: result.user
                }
            })
        }).catch(function(error) {
            console.log(error)
        });
    }

    render() {
        return (
            <Pane display="flex" paddingY="2vh" paddingX="10vw" background="tint2" borderRadius={3}>
                <Pane flex={1} alignItems="center" display="flex">
                    <Link to="/" style={{ textDecoration: 'none' }}>
                        <Tab size={600} marginRight={25} isSelected={this.props.location.pathname === '/'}>
                            Home
                        </Tab>
                    </Link>
                    <Link to="/about" style={{ textDecoration: 'none' }}>
                        <Tab size={600} isSelected={this.props.location.pathname === '/about'} >
                            About
                        </Tab>
                    </Link>
                </Pane>
                <Pane>
                    {this.state.auth.user && this.state.auth.accessToken ?
                    <Text size={600}>Welcome, {this.state.auth.user.displayName}</Text> :
                    <Tab size={600} onSelect={() => this.login()}>Login</Tab>}
                </Pane>
            </Pane>
        );
    }
}

export default withRouter(Header);
