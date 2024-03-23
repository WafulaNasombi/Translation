import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, SafeAreaView, StatusBar } from 'react-native';
import { COLORS, SIZES } from '../constants';

const FrontPage = ({ navigation }) => {
    const navigateToLearning = () => {
        navigation.navigate('ChatPage');
    };

    return (
        <SafeAreaView style={styles.container}>
            <StatusBar barStyle="light-content" />
            <Image
                source={require('../assets/ke.png')} // Example image path
                style={styles.backgroundImage}
            />
            
            <View style={styles.overlay}>
                {/* Header */}
                <View style={styles.Truecont}>
                    <Text style={styles.true}>Truly KE</Text>
                </View>
                <Text style={styles.header}>Welcome to Learn Kenya's Local Languages</Text>
                <View style={{width:"95%", marginHorizontal:"2.5%"}}>
                    <Text style={styles.introText}>
                        Discover the rich cultural heritage of Kenya through its diverse local languages.
                        Learning these languages opens doors to authentic experiences and deeper connections.
                    </Text>
                </View>


                <View style={styles.languageSection}>
                    <TouchableOpacity onPress={navigateToLearning}>
                        <Text style={styles.languageName}>Luo</Text>
                    </TouchableOpacity>
                    <TouchableOpacity onPress={navigateToLearning}>
                        <Text style={styles.languageName}>Kikuyu</Text>
                    </TouchableOpacity>
                    <TouchableOpacity onPress={navigateToLearning}>
                        <Text style={styles.languageName}>Luhya</Text>
                    </TouchableOpacity>
                    <TouchableOpacity onPress={navigateToLearning}>
                        <Text style={styles.languageName}>Meru</Text>
                    </TouchableOpacity>

                </View>

         
                <TouchableOpacity style={styles.ctaButton} onPress={navigateToLearning}>
                        <Text style={styles.ctaButtonText}>Get Started</Text>
                </TouchableOpacity>

              
                <View style={styles.footer}>
                    <Text style={styles.footerText}>© 2024 Learn Kenya's Local Languages</Text>
             
                </View>
            </View>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        height:SIZES.height,
        width:SIZES.width,
        paddingHorizontal: SIZES.padding,
        backgroundColor: "#6bbd99",
    },
    backgroundImage: {
        width:SIZES.width,
        height:SIZES.height*0.5,
        resizeMode: 'cover',
    },
    overlay: {
        ...StyleSheet.absoluteFillObject,
        backgroundColor: 'rgba(0, 0, 0, 0.3)', // Dark overlay to make text readable
        paddingHorizontal: SIZES.padding,
        justifyContent: 'center',
    },
    Truecont:{
        height:SIZES.height*0.13,
        marginTop: -SIZES.height*0.24,
    },
    true:{
        fontSize: 50,
        fontFamily: 'bold',
        marginBottom: 20,
        color: "#fff",
        textAlign: 'center',
        paddingTop: -100,
    },
    header: {
        fontSize: 26,
        fontFamily: 'bold',
        marginBottom: 20,
        color: COLORS.secondary,
        textAlign: 'center',

    },
  
    introText: {
        textAlign: 'center',
        marginBottom: 30,
        color: COLORS.secondary,
        fontFamily: 'semibold',

    },
    languageSection: {
        marginTop: 20,
    },
    languageName: {
        fontSize: 20,
        textAlign: 'center',
        marginTop: 10,
        color: COLORS.secondary,
        fontFamily: 'semibold',

    },
    ctaButton: {
        backgroundColor: COLORS.primary,
        paddingHorizontal: 20,
        paddingVertical: 10,
        borderRadius: 5,
        alignSelf: 'center', // Center the button horizontally
        position: 'absolute',
        bottom: 80,
        marginBottom: 50,
    },
    ctaButtonText: {
        color: COLORS.secondary,
        fontSize: 16,
        fontFamily: 'bold',
    },
    footer: {
        position: 'absolute',
        bottom: 10,
        marginBottom: 30,
        width: SIZES.width,
    },
    footerText: {
        color: COLORS.gray,
        textAlign: 'center',
    },
});

export default FrontPage;
