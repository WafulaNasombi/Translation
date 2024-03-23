import React from 'react';
import { TouchableOpacity, View, StyleSheet } from 'react-native';
import { COLORS, SIZES } from '../constants';
import { Ionicons } from '@expo/vector-icons';

const SendBtn = ({ onPress }) => {
    return (
        <View style={styles.btnCont}>
            <TouchableOpacity
                style={styles.button}
                onPress={onPress}
            >
                <Ionicons name="send" size={24} color="#FFFFFF" />
            </TouchableOpacity>
        </View>
    );
};

export default SendBtn;

const styles = StyleSheet.create({
    btnCont: {
        width: SIZES.width * 0.2,
        height: 50,
        position: 'absolute',
        bottom: 0,
        right: 0,
        marginBottom: 10,
        marginHorizontal: 10,
    },
    button: {
        width: '100%', // Make the button take up the full width of its container
        height: '100%', // Make the button take up the full height of its container
        backgroundColor: COLORS.primary,
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 5,
    },
    buttonText: {
        color: '#FFFFFF',
        fontSize: 16,
        fontWeight: 'bold',
    },
});
