import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation, Outlet } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { OrderProvider } from './context/OrderContext';
import { Navbar } from './components/common/Navbar';
import { Footer } from './components/common/Footer';
import { DemoBanner } from './components/common/DemoBanner';

// Customer Pages
import { HomePage } from './pages/customer/HomePage';
import { MenuPage } from './pages/customer/MenuPage';
import { CartPage } from './pages/customer/CartPage';
import { CheckoutPage } from './pages/customer/CheckoutPage';
import { OrderTrackingPage } from './pages/customer/OrderTrackingPage';
import { CustomerProfilePage } from './pages/customer/CustomerProfilePage';

// Auth Pages
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';

// Management Dashboard Pages
import { DashboardLayout } from './pages/management/DashboardLayout';
import { DashboardHome } from './pages/management/DashboardHome';
import { OrdersManagementPage } from './pages/management/OrdersManagementPage';
import { PosOrderEntryPage } from './pages/management/PosOrderEntryPage';
import { InventoryPage } from './pages/management/InventoryPage';
import { PurchasesPage } from './pages/management/PurchasesPage';
import { SalesExpensesPage } from './pages/management/SalesExpensesPage';
import { CustomerRetentionPage } from './pages/management/CustomerRetentionPage';
import { MenuManagementPage } from './pages/management/MenuManagementPage';
import { SettingsPage } from './pages/management/SettingsPage';
import { DocumentationPage } from './pages/management/DocumentationPage';

// Helper to scroll to top on route change
function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
}

// Customer Layout with Header & Footer
const CustomerLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-brand-cream text-brand-brown">
      <DemoBanner />
      <Navbar />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <OrderProvider>
          <BrowserRouter>
            <ScrollToTop />
            <Routes>
              {/* Customer Experience Routes */}
              <Route path="/" element={<CustomerLayout />}>
                <Route index element={<HomePage />} />
                <Route path="menu" element={<MenuPage />} />
                <Route path="cart" element={<CartPage />} />
                <Route path="checkout" element={<CheckoutPage />} />
                <Route path="track" element={<OrderTrackingPage />} />
                <Route path="profile" element={<CustomerProfilePage />} />
                <Route path="login" element={<LoginPage />} />
                <Route path="register" element={<RegisterPage />} />
              </Route>

              {/* Management Dashboard Experience Routes */}
              <Route path="/dashboard" element={<DashboardLayout />}>
                <Route index element={<DashboardHome />} />
                <Route path="orders" element={<OrdersManagementPage />} />
                <Route path="pos" element={<PosOrderEntryPage />} />
                <Route path="menu" element={<MenuManagementPage />} />
                <Route path="inventory" element={<InventoryPage />} />
                <Route path="purchases" element={<PurchasesPage />} />
                <Route path="sales-expenses" element={<SalesExpensesPage />} />
                <Route path="customers" element={<CustomerRetentionPage />} />
                <Route path="settings" element={<SettingsPage />} />
                <Route path="docs" element={<DocumentationPage />} />
              </Route>

              {/* Fallback */}
              <Route path="*" element={<CustomerLayout />}>
                <Route path="*" element={<HomePage />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </OrderProvider>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;

