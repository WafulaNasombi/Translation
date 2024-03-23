import ChatPage from './screens/ChatPage';
import FrontPage from './screens/FrontPage';
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { useFonts } from 'expo-font';
// import 'react-native-gesture-handler';

export default function App() {
  const [loaded] = useFonts({
    regular:require("./assets/fonts/Poppins-Regular.ttf"),
    light:require("./assets/fonts/Poppins-Light.ttf"),
    bold:require("./assets/fonts/Poppins-Bold.ttf"),
    medium:require("./assets/fonts/Poppins-Medium.ttf"),
    extrabold:require("./assets/fonts/Poppins-ExtraBold.ttf"),
    semibold:require("./assets/fonts/Poppins-SemiBold.ttf"),
  })
  if (!loaded) {
    return null;
  }
  const Stack = createStackNavigator();
  return (
    <NavigationContainer>
    <Stack.Navigator initialRouteName="FrontPage">
      <Stack.Screen
        name="FrontPage"
        component={FrontPage}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name="ChatPage"
        component={ChatPage}
        options={{ headerShown: false }}
      />
    </Stack.Navigator>
  </NavigationContainer>
  );
}


