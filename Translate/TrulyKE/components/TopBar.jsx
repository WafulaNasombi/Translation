import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../constants';

const TopBar = ({ title }) => {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>Luo screen</Text>
        </View>
    );
};

export default TopBar;

const styles = StyleSheet.create({
    container: {
        backgroundColor: COLORS.primary, 
        height: 80, 
        justifyContent: 'center', 
        alignItems: 'center' 
    },
    text:{ 
        color: COLORS.secondary, 
        fontSize: 28, 
        fontFamily: 'semibold', 
        marginTop: 30
    }
}); 
